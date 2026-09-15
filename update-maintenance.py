#!/usr/bin/env python3
"""Query 車輛維修記錄 Notion DB and output as gg-maintenance.json"""
import json, os, urllib.request
from datetime import datetime, timezone

with open(os.path.expanduser('~/.config/notion/api_key')) as f:
    TOKEN = f.read().strip()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

DB_ID = "cc006950-e4b8-4772-ae4f-5a6b5c1a6eda"

# Query all records
req = urllib.request.Request(
    f"https://api.notion.com/v1/databases/{DB_ID}/query",
    data=json.dumps({"page_size": 50}).encode(),
    headers=HEADERS
)

try:
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
except Exception as e:
    print(json.dumps({"error": str(e), "items": []}))
    exit(1)

now = datetime.now()
items = []

for page in data.get('results', []):
    props = page.get('properties', {})
    
    def get_title(name):
        titles = props.get(name, {}).get('title', [])
        return titles[0]['plain_text'] if titles else ''
    
    def get_rich(name):
        texts = props.get(name, {}).get('rich_text', [])
        return texts[0]['plain_text'] if texts else ''
    
    def get_select(name):
        s = props.get(name, {}).get('select')
        return s['name'] if s else ''
    
    def get_number(name):
        return props.get(name, {}).get('number')
    
    def get_date(name):
        d = props.get(name, {}).get('date')
        if d and d.get('start'):
            return d['start']
        return None
    
    def get_multi(name):
        return [m['name'] for m in props.get(name, {}).get('multi_select', [])]
    
    vehicle = get_title('Vehicle')
    part_service = get_rich('Part / Service')
    component = get_multi('Component')
    interval = get_number('Interval (Months)')
    last_service = get_date('Last Service Date')
    reminder = get_date('Reminder')
    notes = get_rich('Notes')
    company = get_rich('Company')
    cost = get_number('Cost (HKD)')
    
    # Calculate next service due
    next_service = None
    due_status = 'ok'
    if last_service and interval:
        last = datetime.fromisoformat(last_service)
        # Calculate next due
        import calendar
        month = last.month + interval
        year = last.year + (month - 1) // 12
        month = ((month - 1) % 12) + 1
        day = min(last.day, calendar.monthrange(year, month)[1])
        from datetime import timedelta
        next_dt = last.replace(year=year, month=month, day=day)
        next_service = next_dt.strftime('%Y-%m-%d')
        
        days_until = (next_dt - now).days
        if days_until < 0:
            due_status = f'overdue {abs(days_until)}d'
        elif days_until <= 30:
            due_status = f'{days_until}d'
        else:
            due_status = next_service
    
    items.append({
        'vehicle': vehicle,
        'service': part_service,
        'component': component[0] if component else vehicle,
        'interval': interval,
        'lastService': last_service,
        'nextService': next_service,
        'dueStatus': due_status,
        'reminder': reminder,
        'notes': notes,
        'company': company,
        'cost': cost
    })

# Sort by urgency (overdue first, then soonest)
def sort_key(item):
    ds = item['dueStatus']
    if 'overdue' in ds:
        return 0, -int(ds.split()[1].rstrip('d'))
    if ds == 'ok':
        return 2, 0
    try:
        return 1, int(ds.rstrip('d'))
    except:
        return 3, 0

items.sort(key=sort_key)

output = {
    "ts": datetime.now().strftime('%H:%M'),
    "total": len(items),
    "items": items
}

print(json.dumps(output, ensure_ascii=False))
