#!/usr/bin/env python3
"""
GG API Connector — 統一 API connection 管理
自動 refresh token、reconnect、error handling
所有 scripts 共用呢個 module

Usage:
    from scripts.api_connector import GoogleAPI, MSApi, NotionAPI
    gapi = GoogleAPI()
    events = gapi.get_events(cal_id, time_min, time_max)
    
    ms = MSApi()
    tasks = ms.get_tasks()
"""

import json, os, urllib.request, urllib.parse, urllib.error, time
from pathlib import Path
from datetime import datetime, timedelta, timezone, date

WORKSPACE = Path('/home/airoot/.openclaw/workspace')
CONFIG_DIR = WORKSPACE / 'config'
SCRIPTS_DIR = WORKSPACE / 'scripts'

# === Time ===
def hkt_now():
    """Get current HKT time using gg_time.py (stdtime.gov.hk NTP)"""
    import sys
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        from gg_time import now
        return now()
    except ImportError:
        return datetime.now(timezone(timedelta(hours=8)))

def utc_to_hkt(utc_dt_str):
    """將 UTC datetime string 轉做 HKT datetime object"""
    try:
        dt = datetime.fromisoformat(utc_dt_str.replace('Z', '+00:00'))
        return dt.astimezone(timezone(timedelta(hours=8)))
    except:
        return None

def today_hkt_str():
    """YYYY-MM-DD in HKT"""
    return hkt_now().strftime('%Y-%m-%d')

def tomorrow_hkt_str():
    """YYYY-MM-DD in HKT (明天)"""
    return (hkt_now() + timedelta(days=1)).strftime('%Y-%m-%d')


class GoogleAPI:
    """Google APIs — Calendar, etc. Auto-refresh token"""
    
    def __init__(self):
        self.token_file = CONFIG_DIR / 'google_calendar_token.json'
        self.client_file = CONFIG_DIR / 'google_calendar_web_client.json'
        self._token = None
        self._client = None
        
    def _load_client(self):
        if not self._client:
            with open(self.client_file) as f:
                self._client = json.load(f)
        return self._client['web']
    
    def _load_token(self):
        if not self._token:
            with open(self.token_file) as f:
                self._token = json.load(f)
        return self._token
    
    def _save_token(self, token):
        self._token = token
        self.token_file.write_text(json.dumps(token, indent=2))
    
    def refresh_token(self):
        """Refresh Google OAuth token"""
        client = self._load_client()
        token = self._load_token()
        
        body = urllib.parse.urlencode({
            'client_id': client['client_id'],
            'client_secret': client['client_secret'],
            'refresh_token': token['refresh_token'],
            'grant_type': 'refresh_token',
        }).encode()
        
        req = urllib.request.Request('https://oauth2.googleapis.com/token', data=body)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                nt = json.loads(r.read())
                token['access_token'] = nt['access_token']
                if 'expires_in' in nt:
                    token['expires_at'] = time.time() + nt['expires_in']
                self._save_token(token)
                return token['access_token']
        except Exception as e:
            raise ConnectionError(f"Google token refresh failed: {e}")
    
    def get_access_token(self):
        """Get valid access token, refresh if needed"""
        token = self._load_token()
        expires_at = token.get('expires_at', 0)
        
        # Refresh if expired or within 60s of expiry
        if time.time() >= expires_at - 60:
            return self.refresh_token()
        return token['access_token']
    
    def _request(self, url, method='GET', data=None, retries=2):
        """Make authed request with auto-retry on 401"""
        for attempt in range(retries):
            try:
                access_token = self.get_access_token()
                req = urllib.request.Request(url, data=data)
                req.add_header('Authorization', f'Bearer {access_token}')
                req.add_header('Content-Type', 'application/json')
                
                if method == 'PATCH':
                    req.method = 'PATCH'
                
                with urllib.request.urlopen(req, timeout=10) as r:
                    return json.loads(r.read())
                
            except urllib.error.HTTPError as e:
                if e.code == 401 and attempt < retries - 1:
                    # Token expired, force refresh and retry
                    self.refresh_token()
                    continue
                raise ConnectionError(f"Google API {e.code}: {e.reason} — {url[:60]}")
            except urllib.error.URLError as e:
                if attempt < retries - 1:
                    time.sleep(1)
                    continue
                raise ConnectionError(f"Google API connection failed: {e.reason}")
        return None
    
    # Calendar
    def list_calendars(self):
        url = 'https://www.googleapis.com/calendar/v3/users/me/calendarList'
        return self._request(url)
    
    def get_events(self, cal_id, time_min, time_max):
        """Get events between time_min and time_max (RFC3339 format with +08:00)"""
        url = ('https://www.googleapis.com/calendar/v3/calendars/'
               + urllib.parse.quote(cal_id, safe='')
               + '/events?orderBy=startTime&singleEvents=true'
               + '&timeMin=' + urllib.parse.quote(time_min)
               + '&timeMax=' + urllib.parse.quote(time_max))
        return self._request(url)
    
    def get_events_today(self, cal_id):
        """Get today's events for a calendar"""
        hkt = hkt_now()
        day_start = hkt.strftime('%Y-%m-%dT00:00:00+08:00')
        day_end = hkt.strftime('%Y-%m-%dT23:59:00+08:00')
        return self.get_events(cal_id, day_start, day_end)
    
    def update_event_reminder(self, cal_id, event_id, reminders):
        """Update event reminders. reminders format: [{'method':'popup','minutes':30}]"""
        url = ('https://www.googleapis.com/calendar/v3/calendars/'
               + urllib.parse.quote(cal_id, safe='')
               + '/events/' + urllib.parse.quote(event_id, safe=''))
        data = json.dumps({
            'reminders': {
                'useDefault': False,
                'overrides': reminders
            }
        }).encode()
        return self._request(url, method='PATCH', data=data)
    
    def create_event(self, cal_id, summary, start_iso, end_iso, reminders=None, description=''):
        """Create a calendar event"""
        event = {
            'summary': summary,
            'start': {'dateTime': start_iso, 'timeZone': 'Asia/Hong_Kong'},
            'end': {'dateTime': end_iso, 'timeZone': 'Asia/Hong_Kong'},
            'description': description,
        }
        if reminders:
            event['reminders'] = {'useDefault': False, 'overrides': reminders}
        
        url = ('https://www.googleapis.com/calendar/v3/calendars/'
               + urllib.parse.quote(cal_id, safe='')
               + '/events')
        data = json.dumps(event).encode()
        return self._request(url, method='POST', data=data)


class MSApi:
    """Microsoft Graph API — To Do, Calendar, etc. Auto-refresh token"""
    
    def __init__(self):
        self.token_file = CONFIG_DIR / 'ms_graph_token.json'
        self.client_id = '014876ab-9543-4a4e-908d-e9fd62796ff3'
        self._token = None
        self._tenant = '9188040d-6c67-4c5b-b112-36a304b66dad'  # MSA (personal)
        
    def _load_token(self):
        if not self._token:
            with open(self.token_file) as f:
                self._token = json.load(f)
        return self._token
    
    def _save_token(self, token):
        self._token = token
        self.token_file.write_text(json.dumps(token, indent=2))
    
    def refresh_token(self):
        """Refresh MS Graph token"""
        token = self._load_token()
        
        body = urllib.parse.urlencode({
            'client_id': self.client_id,
            'refresh_token': token['refresh_token'],
            'grant_type': 'refresh_token',
            'redirect_uri': 'http://localhost',
            'client_info': '1',
        }).encode()
        
        # Try both common and MSA tenant
        for tenant in ['9188040d-6c67-4c5b-b112-36a304b66dad', 'common']:
            try:
                url = f'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token'
                req = urllib.request.Request(url, data=body)
                req.add_header('Content-Type', 'application/x-www-form-urlencoded')
                
                with urllib.request.urlopen(req, timeout=5) as r:
                    nt = json.loads(r.read())
                    token['access_token'] = nt['access_token']
                    if 'refresh_token' in nt:
                        token['refresh_token'] = nt['refresh_token']
                    if 'expires_in' in nt:
                        token['expires_at'] = time.time() + nt['expires_in']
                    self._save_token(token)
                    return token['access_token']
            except:
                continue
        
        raise ConnectionError("MS token refresh failed (all tenants)")
    
    def get_access_token(self):
        token = self._load_token()
        expires_at = token.get('expires_at', 0)
        if time.time() >= expires_at - 120:
            return self.refresh_token()
        return token['access_token']
    
    def _request(self, url, method='GET', data=None, retries=2):
        for attempt in range(retries):
            try:
                access_token = self.get_access_token()
                req = urllib.request.Request(url, data=data)
                req.add_header('Authorization', f'Bearer {access_token}')
                
                if data:
                    req.add_header('Content-Type', 'application/json')
                if method == 'PATCH':
                    req.method = 'PATCH'
                if method == 'POST':
                    req.method = 'POST'
                if method == 'DELETE':
                    req.method = 'DELETE'
                
                with urllib.request.urlopen(req, timeout=10) as r:
                    return json.loads(r.read())
                
            except urllib.error.HTTPError as e:
                if e.code == 401 and attempt < retries - 1:
                    self.refresh_token()
                    continue
                # 404 = not found, often expected
                if e.code == 404:
                    return None
                raise ConnectionError(f"MS API {e.code}: {e.reason} — {url[:60]}")
            except urllib.error.URLError as e:
                if attempt < retries - 1:
                    time.sleep(1)
                    continue
                raise ConnectionError(f"MS API connection failed: {e.reason}")
        return None
    
    # To Do
    def list_tasks_lists(self):
        url = 'https://graph.microsoft.com/v1.0/me/todo/lists'
        return self._request(url)
    
    def get_tasks(self, list_id=None):
        """Get incomplete tasks from a list, or all lists"""
        if list_id:
            url = 'https://graph.microsoft.com/v1.0/me/todo/lists/' + urllib.parse.quote(list_id, safe='') + '/tasks'
            result = self._request(url)
            if not result:
                return []
            return [t for t in result.get('value', []) if t.get('status') != 'completed']
        
        # Get all lists + tasks
        all_tasks = []
        lists = self.list_tasks_lists()
        for tl in lists.get('value', []):
            tasks = self.get_tasks(tl['id'])
            for t in tasks:
                t['_list_name'] = tl['displayName']
                t['_list_id'] = tl['id']
            all_tasks.extend(tasks)
        return all_tasks
    
    def add_task(self, list_id, title, due_date=None, importance='normal', body=''):
        """Add a task. due_date: 'YYYY-MM-DD' or datetime"""
        if list_id is None:
            # Find 'TODO' list
            lists = self.list_tasks_lists()
            for tl in lists.get('value', []):
                if tl['displayName'] == 'TODO':
                    list_id = tl['id']
                    break
        
        if not list_id:
            raise ValueError("No list found")
        
        # MS Graph uses lowercase importance: 'low', 'normal', 'high'
        valid_importance = {'low', 'normal', 'high'}
        imp = str(importance).lower()
        if imp not in valid_importance:
            imp = 'normal'
        task = {'title': title, 'importance': imp, 'status': 'notStarted'}
        if due_date:
            if isinstance(due_date, str):
                if 'T' in due_date:
                    dt = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                else:
                    dt = datetime.fromisoformat(due_date)
            else:
                dt = due_date
            task['dueDateTime'] = {
                'dateTime': dt.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'Asia/Hong_Kong'
            }
        if body:
            task['body'] = {'content': body, 'contentType': 'text'}
        
        url = 'https://graph.microsoft.com/v1.0/me/todo/lists/' + urllib.parse.quote(list_id, safe='') + '/tasks'
        return self._request(url, method='POST', data=json.dumps(task).encode())
    
    def complete_task(self, list_id, task_id):
        """Mark task as completed"""
        url = 'https://graph.microsoft.com/v1.0/me/todo/lists/' + urllib.parse.quote(list_id, safe='') + '/tasks/' + urllib.parse.quote(task_id, safe='')
        data = json.dumps({'status': 'completed'}).encode()
        return self._request(url, method='PATCH', data=data)
    
    def update_task(self, list_id, task_id, updates):
        """Update task fields. updates: dict like {'dueDateTime': {...}}"""
        url = 'https://graph.microsoft.com/v1.0/me/todo/lists/' + urllib.parse.quote(list_id, safe='') + '/tasks/' + urllib.parse.quote(task_id, safe='')
        return self._request(url, method='PATCH', data=json.dumps(updates).encode())


class NotionAPI:
    """Notion API — Read/write databases"""
    
    def __init__(self):
        self.key_file = CONFIG_DIR / 'notion' / 'api_key'
        self.version = '2022-06-28'
        self._key = None
        
    def _get_key(self):
        if not self._key:
            with open(self.key_file) as f:
                self._key = f.read().strip()
        return self._key
    
    def _request(self, url, data=None, method='POST'):
        key = self._get_key()
        req = urllib.request.Request(url, data=data)
        req.add_header('Authorization', f'Bearer {key}')
        req.add_header('Notion-Version', self.version)
        req.add_header('Content-Type', 'application/json')
        if method != 'POST':
            req.method = method
        
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            raise ConnectionError(f"Notion API {e.code}: {e.reason}")
    
    def search(self, query=''):
        """Search Notion (databases, pages)"""
        data = json.dumps({
            'filter': {'value': 'data_source', 'property': 'object'},
            'page_size': 50
        }).encode()
        return self._request('https://api.notion.com/v1/search', data=data)
    
    def query_database(self, db_id, page_size=50):
        data = json.dumps({'page_size': page_size}).encode()
        url = f'https://api.notion.com/v1/databases/{db_id}/query'
        return self._request(url, data=data)


# === Convenience functions ===

def get_calendar_id(name):
    """Get calendar ID by display name"""
    cals = {
        'KINETIX': 'bdf77584e15d456a0187a4515a801fb126ddd9f151889904ab24342bd1859418@group.calendar.google.com',
        '青成敬拜隊': '4645b705527f06f39b79c0937791065f6b718875a0fcbd89f9cfd3fa2c7b615f@group.calendar.google.com',
        'primary': 'primary',
    }
    # Also try to search dynamically via Google API
    return cals.get(name, 'primary')


def test_connections():
    """Test all API connections"""
    results = {}
    
    try:
        gapi = GoogleAPI()
        gapi.list_calendars()
        results['Google'] = '✅'
    except Exception as e:
        results['Google'] = f'❌ {e}'
    
    try:
        ms = MSApi()
        ms.list_tasks_lists()
        results['MS Graph'] = '✅'
    except Exception as e:
        results['MS Graph'] = f'❌ {e}'
    
    try:
        napi = NotionAPI()
        napi.search()
        results['Notion'] = '✅'
    except Exception as e:
        results['Notion'] = f'❌ {e}'
    
    print('=== API Connection Test ===')
    for name, status in results.items():
        print(f'  {name}: {status}')
    return results


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test_connections()
    elif len(sys.argv) > 1 and sys.argv[1] == 'google-test':
        gapi = GoogleAPI()
        cals = gapi.list_calendars()
        print(f'Google Calendar: {len(cals.get("items",[]))} calendars found')
        for cal in cals.get('items', [])[:5]:
            print(f'  - {cal.get("summary", "?")}')
    elif len(sys.argv) > 1 and sys.argv[1] == 'ms-test':
        ms = MSApi()
        lists = ms.list_tasks_lists()
        print(f'MS To Do: {len(lists.get("value",[]))} lists')
        for tl in lists.get('value', []):
            tasks = ms.get_tasks(tl['id'])
            print(f'  - {tl["displayName"]}: {len(tasks)} incomplete tasks')
    else:
        print(f'GG API Connector — hkt_now: {hkt_now().strftime("%Y-%m-%d %H:%M:%S HKT")}')
        print('Commands: test, google-test, ms-test')
