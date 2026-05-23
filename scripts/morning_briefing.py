#!/usr/bin/env python3
"""
GG Morning Briefing - 朝早綜合報告
整合：HKO (天氣)、Google Maps Routes API (交通)、Calendar (日程)、Notion (合約)
"""
import json, urllib.request, urllib.parse, sys, os, re, traceback, subprocess
from datetime import datetime, timezone, timedelta
sys.path.insert(0, '/home/airoot/.openclaw/workspace/scripts')
import gg_time

HKT = timezone(timedelta(hours=8))

# ─── API Key ───
GMAPS_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')
if not GMAPS_KEY:
    # Try multiple sources (crontab runs as root, no user env)
    sources = [
        '~/.openclaw/.env',               # OpenClaw global env
        '~/.bashrc',
        '~airoot/.bashrc',
        '~root/.bashrc',
    ]
    for src in sources:
        try:
            result = subprocess.run(
                ['bash', '-c', f'source {src} 2>/dev/null; echo $GOOGLE_MAPS_API_KEY'],
                capture_output=True, text=True, timeout=10
            )
            loaded = result.stdout.strip()
            if loaded:
                GMAPS_KEY = loaded
                break
        except Exception:
            continue

if not GMAPS_KEY:
    print('ERROR: GOOGLE_MAPS_API_KEY not found.', file=sys.stderr)
    sys.exit(1)

CONTRACTS_DB = "29d783d5-93e7-8056-93fb-cd6756c2acc2"

# Coordinates
HOME = "22.441569,114.063731"       # 錦田水尾村
OFFICE = "22.312676,114.226162"     # 觀塘AIA大樓

ROAD_SEGMENTS = [
    (["錦田","水頭","錦慶","元朗"], "錦田→元朗"),
    (["大欖","青朗"], "大欖隧道"),
    (["汀九","長青","長青隧道"], "汀九→長青"),
    (["荃灣"], "荃灣路"),
    (["葵涌","荔枝角"], "葵涌道→荔枝角"),
    (["西九龍"], "西九龍公路"),
    (["油麻地","中九龍","窩打老道","九龍塘"], "中九龍繞道"),
    (["啓德","啓福","九龍灣","麗晶"], "啓德→九龍灣"),
    (["觀塘道","繞道","牛頭角"], "觀塘道"),
    (["開源","巧明","鴻圖"], "到公司"),
]

def _parse_min(txt):
    if not txt: return 0
    nums = re.findall(r'(\d+)', txt)
    total = 0
    if 'hour' in txt or '時間' in txt or '小時' in txt:
        total += int(nums[0]) * 60; nums = nums[1:]
    if nums: total += int(nums[0])
    return total

def _icon_for_delay(delay_s):
    if delay_s <= 0: return '🟢'
    elif delay_s <= 120: return '🟡'
    elif delay_s <= 300: return '🔶'
    else: return '🔴'

def _call_routes_api(origin, dest, traffic_aware=True):
    if not GMAPS_KEY: return None
    fields = ("routes.duration,routes.distanceMeters,"
              "routes.legs.duration,routes.legs.distanceMeters,"
              "routes.legs.steps.distanceMeters,routes.legs.steps.staticDuration,"
              "routes.legs.steps.navigationInstruction")
    if traffic_aware: fields += ",routes.travelAdvisory"

    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    future = (datetime.now(HKT) + timedelta(minutes=2)).isoformat()
    body = {
        "origin": {"location": {"latLng": {"latitude": float(origin.split(",")[0]), "longitude": float(origin.split(",")[1])}}},
        "destination": {"location": {"latLng": {"latitude": float(dest.split(",")[0]), "longitude": float(dest.split(",")[1])}}},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE" if traffic_aware else "TRAFFIC_UNAWARE",
        "departureTime": future if traffic_aware else None,
        "languageCode": "zh-TW",
        "units": "IMPERIAL",
    }
    if not traffic_aware:
        del body["departureTime"]

    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type":"application/json","X-Goog-Api-Key":GMAPS_KEY,"X-Goog-FieldMask":fields},
                                 method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except: return None

# =======================
# 1. WEATHER
# =======================
def get_weather():
    try:
        req = urllib.request.Request(
            "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=tc",
            headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            w = json.loads(r.read())

        temp = None
        for s in w.get("temperature",{}).get("data",[]):
            if s.get("place")=="元朗公園": temp=s.get("value"); break
        if not temp:
            for s in w.get("temperature",{}).get("data",[]):
                if s.get("place") in ["彩虹","觀塘","九龍城"]: temp=s.get("value"); break
        temp_str = f"{temp}°C" if temp else ""

        humidity = w.get("humidity",{}).get("data",[{}])[0].get("value")
        humid_str = f"濕度{humidity}%" if humidity else ""

        max_rain = max((r.get("max",0) for r in w.get("rainfall",{}).get("data",[])), default=-1)
        rain_str = "今日有雨，帶遮 🌂" if max_rain>0 else ("今日無雨" if max_rain==0 else "")

        icon_map = {"50":"☀️","51":"🌤","52":"⛅","53":"🌥","54":"☁️","60":"🌧","61":"🌦","62":"🌦","63":"🌧","64":"🌧","65":"🌧","70":"🌫","80":"⛈","81":"⛈","82":"⛈","83":"🌦","84":"🌦","85":"🌦","90":"🌩"}
        icon_str = icon_map.get(str(w.get("icon",0)), "")

        warnings = []
        for mt in ["rainstorm","tc","frost","fire","tsunami","flooding"]:
            msg = w.get("message",{}).get(mt,"")
            if msg: warnings.append(msg)

        return {"temp":temp_str,"humidity":humid_str,"rain_str":rain_str,"icon":icon_str,"warnings":warnings}
    except Exception as e:
        traceback.print_exc()
        return {"error":str(e),"temp":"","humidity":"","rain_str":"","icon":"","warnings":[]}

# =======================
# 2. TRAFFIC
# =======================
def get_traffic():
    out = {"drive": None, "drive_detail": [], "transit": []}

    # Routes API: traffic vs normal
    data_t = _call_routes_api(HOME, OFFICE, True)
    data_n = _call_routes_api(HOME, OFFICE, False)

    if data_t and "routes" in data_t and data_t["routes"]:
        r = data_t["routes"][0]
        leg = r.get("legs",[{}])[0]
        dur_t = r.get("duration","") or leg.get("duration","")
        dur_t_s = int(dur_t.replace("s","")) if isinstance(dur_t,str) and dur_t.endswith("s") else 0
        dur_n_s = 0
        if data_n and "routes" in data_n and data_n["routes"]:
            rn = data_n["routes"][0]
            dur_n = rn.get("duration","")
            dur_n_s = int(dur_n.replace("s","")) if isinstance(dur_n,str) and dur_n.endswith("s") else 0
        dist_m = leg.get("distanceMeters",0)
        dist_km = dist_m/1000
        delay = dur_t_s-dur_n_s

        if dur_t_s>0:
            out["drive"] = f"約{dur_t_s//60}分鐘（{dist_km:.1f}km）"
            if dur_n_s>0: out["drive"] += f"，正常約{dur_n_s//60}分鐘"
            if delay>60: out["drive"] += f"，比正常慢{delay//60}分鐘"

        steps = leg.get("steps",[])
        if steps:
            seg={}
            for s in steps:
                instr = s.get("navigationInstruction",{}).get("instructions","")
                sd = s.get("staticDuration","0s")
                sd_v = int(sd.replace("s","")) if isinstance(sd,str) else 0
                mt = next((n for kw,n in ROAD_SEGMENTS if any(k in instr for k in kw)), "其他")
                seg[mt] = seg.get(mt,0)+sd_v
            total = sum(seg.values())
            seg_lines=[]
            for name in ["錦田→元朗","大欖隧道","汀九→長青","荃灣路","葵涌道→荔枝角","西九龍公路","中九龍繞道","啓德→九龍灣","觀塘道","到公司"]:
                if name in seg and total>0:
                    mn = round(seg[name]/60)
                    sd = round(delay*seg[name]/total) if total>0 else 0
                    seg_lines.append(f"{_icon_for_delay(sd)} {name}: ~{mn}min")
            out["drive_detail"] = seg_lines

    # Directions API fallback
    elif data_n is not None:
        dr = None
        try:
            o=urllib.parse.quote("錦田水尾村"); d=urllib.parse.quote("觀塘AIA大樓")
            url=f"https://maps.googleapis.com/maps/api/directions/json?origin={o}&destination={d}&mode=driving&departure_time=now&traffic_model=best_guess&key={GMAPS_KEY}"
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req,timeout=10) as r: dr=json.loads(r.read())
        except: pass
        if dr and dr.get("status")=="OK":
            leg=dr["routes"][0]["legs"][0]
            dur_t=leg.get("duration_in_traffic",leg["duration"]).get("text","")
            dur_n=leg["duration"]["text"]; dist=leg["distance"]["text"]
            diff=_parse_min(dur_t)-_parse_min(dur_n)
            out["drive"]=f"{dur_t}（{dist}）"
            if diff>1: out["drive"]+=f"，比正常慢{diff}分鐘"
            for step in leg.get("steps",[]):
                instr=re.sub(r'<[^>]+>','',step.get("html_instructions",""))
                st=_parse_min(step.get("duration",{}).get("text",""))
                mt=next((n for kw,n in ROAD_SEGMENTS if any(k in instr for k in kw)),None)
                if mt: out["drive_detail"].append(f"🟡 {mt}: ~{st}min")
        else:
            out["drive"]="無法取得交通數據"
    else:
        out["drive"]="無法取得交通數據"

    # Transit
    for tr in [{"k":"601B","o":"錦田郵局","d":"觀塘AIA"},{"k":"Tuen Ma","o":"錦上路站","d":"觀塘港鐵站"}]:
        try:
            o=urllib.parse.quote(tr["o"]); d=urllib.parse.quote(tr["d"])
            url=f"https://maps.googleapis.com/maps/api/directions/json?origin={o}&destination={d}&mode=transit&departure_time=now&key={GMAPS_KEY}&language=zh-TW"
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req,timeout=10) as r: t=json.loads(r.read())
            if t.get("status")=="OK":
                leg=t["routes"][0]["legs"][0]
                out["transit"].append({"key":tr["k"],"depart":leg["departure_time"]["text"],"arrive":leg["arrival_time"]["text"],"duration":leg["duration"]["text"],"secs":leg["duration"]["value"]})
        except: pass
    out["transit"].sort(key=lambda x:x.get("secs",9999))
    return out

# =======================
# 3. NOTION CONTRACTS
# =======================
def get_renewals():
    from api_connector import NotionAPI
    now = gg_time.now()
    today = now.strftime("%Y-%m-%d")
    future = (now+timedelta(days=30)).strftime("%Y-%m-%d")
    payload={"page_size":100,"filter":{"and":[{"property":"Remind date","date":{"is_not_empty":True}},{"property":"Remind date","date":{"on_or_after":today}},{"property":"Remind date","date":{"on_or_before":future}}]},"sorts":[{"property":"Remind date","direction":"ascending"}]}
    try:
        napi=NotionAPI()
        data=napi._request(f"https://api.notion.com/v1/databases/{CONTRACTS_DB}/query",data=json.dumps(payload).encode())
    except: return []
    results=[]
    now_n=now.replace(tzinfo=None)
    for item in data.get("results",[]):
        p=item["properties"]
        name=p.get("Items",{}).get("title",[{}])[0].get("text",{}).get("content","N/A")
        remind=p.get("Remind date",{}).get("date",{})
        remind_str=remind.get("start") if remind else None
        cost=p.get("Cost",{}).get("number")
        if remind_str:
            try:
                dt=datetime.strptime(remind_str,"%Y-%m-%d")
                days=(dt-now_n).days
                if 0<=days<=30:
                    cost_str=f" ${cost:,.0f}" if cost else ""
                    tag="今日到期" if days==0 else "聽日到期" if days==1 else f"{days}日後到期"
                    results.append(f"{tag} — {name}{cost_str}")
            except: pass
    return results

# =======================
# 4. CALENDAR
# =======================
def get_calendar():
    try:
        from api_connector import GoogleAPI
        gapi=GoogleAPI()
        now=gg_time.now()
        s=now.strftime("%Y-%m-%dT00:00:00+08:00")
        e=now.strftime("%Y-%m-%dT23:59:00+08:00")
        data=gapi.get_events("primary",s,e)
        if not data: return None
        events=[]
        for item in data.get("items",[]):
            start=item.get("start",{}).get("dateTime") or item.get("start",{}).get("date","")
            summary=item.get("summary","")
            if start and summary:
                try:
                    t=datetime.fromisoformat(start.replace("Z","+00:00")).astimezone(HKT)
                    start_str=t.strftime("%H:%M")
                except: start_str=start
                events.append(f"{start_str} {summary}")
        return events
    except: return None

# =======================
# 5. MAIN
# =======================
def main():
    now=gg_time.now()
    print(f"早晨 — {now.strftime('%A %d/%m')}\n")

    w=get_weather()
    if w and "error" not in w:
        parts=[p for p in [w.get("temp",""),w.get("humidity",""),w.get("rain_str",""),w.get("icon","")] if p]
        print(f"天氣: {'｜'.join(parts)}")
        for msg in w.get("warnings",[]): print(f"  ⚠ {msg}")
        print()

    t=get_traffic()
    if t["drive"]:
        print(f"🚗 駕車: {t['drive']}")
        for l in t["drive_detail"]: print(f"  {l}")
        print()

    for tr in t["transit"]:
        if tr.get("key")=="601B":
            print(f"601B→屯馬線→觀塘線: {tr['depart']}→{tr['arrive']}（{tr['duration']}）")
            break
    for tr in t["transit"]:
        if tr.get("key")=="Tuen Ma":
            print(f"屯馬線（步行至錦上路站）→觀塘線: {tr['depart']}→{tr['arrive']}（{tr['duration']}）")
            break
    print()

    cal=get_calendar()
    if cal:
        evs=[e for e in cal if "Hybrid Exchange" not in e]
        if evs: print("今日日程:\n"+"\n".join(f"  {e}" for e in evs[:5]))
        else: print("今日日程: （無特定日程）")
        print()

    renewals=get_renewals()
    if renewals: print("即將到期:\n"+"\n".join(f"  {r}" for r in renewals))
    else: print("即將到期: （無）")
    print()

if __name__=="__main__":
    main()
