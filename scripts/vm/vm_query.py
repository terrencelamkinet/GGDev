#!/usr/bin/env python3
"""
VM Query System - 統一查詢 GG-Work / GG-Person VM
用嚟喺 generate briefing 時從兩邊 VM 拎資料
"""
import json, subprocess, sys, time

VM_CONFIG = {
    "work": {
        "name": "GG-Work 🦾⚙️",
        "agent": "GG-Work",
        "url": "http://127.0.0.1:18901/v1/chat/completions",
        "token": "49ccb297fe1533acf64b4d8925713782be2d58f9b68eb34cdcd50a761473b652"
    },
    "person": {
        "name": "GG-Person 🦾❤️",
        "agent": "GG-Person",
        "url": "http://127.0.0.1:18902/v1/chat/completions",
        "token": "bf80e73561d252ec9345a2be8be7c4c0e952187ef0d4f375202a62de1b3cf8a2"
    }
}

def query_vm(target, prompt, max_tokens=2000, timeout=45):
    """Ask a VM for information (timeout bumped to 45s for production)"""
    vm = VM_CONFIG[target]
    
    payload = {
        "model": f"openclaw/{vm['agent']}",
        "messages": [
            {
                "role": "system",
                "content": f"你係 {vm['name']}，GG 大總管嘅{sub_target_name(target)}記憶專家。"
                            f"大總管問你關於Terrence嘅{target}資訊。"
                            f"請根據你嘅記憶（memory/ 目錄、memory_index.md、Notion）回答。"
                            f"如果冇相關記憶，就話「冇記錄」。"
                            f"回答要簡潔、事實為本。"
            },
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens
    }
    
    cmd = [
        "curl", "-s", "--max-time", str(timeout + 10), vm["url"],
        "-H", f"Authorization: Bearer {vm['token']}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload)
    ]
    
    for attempt in range(2):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            data = json.loads(result.stdout)
            if "choices" in data and len(data["choices"]) > 0:
                return {"ok": True, "content": data["choices"][0]["message"]["content"]}
            if attempt == 0 and "error" in data and "rate" in str(data.get("error","")).lower():
                time.sleep(3)
                continue
            return {"ok": False, "error": str(data.get("error", "Unknown"))}
        except subprocess.TimeoutExpired:
            if attempt == 0:
                time.sleep(3)
                continue
            return {"ok": False, "error": f"Timeout after {timeout}s (attempt {attempt+1})"}
        except Exception as e:
            if attempt == 0:
                time.sleep(3)
                continue
            return {"ok": False, "error": str(e)}
    
    return {"ok": False, "error": "Max retries exhausted"}

def sub_target_name(target):
    if target == "person": return "個人"
    return "工作"

def collect_morning_data():
    """Collect ALL data needed for morning briefing from both VMs"""
    results = {}
    
    # GG-Person: personal data
    person_queries = [
        ("today", "Terrence今日有咩個人行程或約會？（檢查 memory/ 目錄）"),
        ("reminders", "Terrence今日有咩個人提醒？"),
        ("yesterday", "尋日 Terrence 有咩個人重要對話或事件？")
    ]
    
    # GG-Work: work data
    work_queries = [
        ("tasks", "Terrence今日有咩工作任務或會議？"),
        ("deadlines", "有冇今日到期嘅 deadline？"),
        ("projects", "Active projects 最新 status 係咩？")
    ]
    
    print("📡 Querying GG-Person for personal data...")
    for key, q in person_queries:
        r = query_vm("person", q)
        results[f"person_{key}"] = r.get("content", f"❌ {r.get('error', 'fail')}") if r["ok"] else f"❌ {r['error']}"
        time.sleep(0.5)
    
    print("📡 Querying GG-Work for work data...")
    for key, q in work_queries:
        r = query_vm("work", q)
        results[f"work_{key}"] = r.get("content", f"❌ {r.get('error', 'fail')}") if r["ok"] else f"❌ {r['error']}"
        time.sleep(0.5)
    
    return results

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # CLI mode: query specific VM
        target = sys.argv[1]
        query = " ".join(sys.argv[2:])
        result = query_vm(target, query)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Collect all morning data
        data = collect_morning_data()
        print("\n📊 === COLLECTED DATA ===")
        for key, val in data.items():
            print(f"\n[{key}]:")
            print(f"  {val[:300]}")
