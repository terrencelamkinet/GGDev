"""Smart AI Server — standalone FastAPI server for desktop client."""
import os, json, re, uuid, hashlib, time, urllib.request
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Smart AI Server", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ── Config ──
CFG_DIR = os.path.expanduser("~/.smart-ai")
os.makedirs(CFG_DIR, exist_ok=True)
CFG_PATH = os.path.join(CFG_DIR, "config.json")

def load_cfg():
    try:
        with open(CFG_PATH) as f:
            return json.load(f)
    except:
        return {"llm_api_key": "", "llm_model": "deepseek-chat", "llm_base_url": "https://api.deepseek.com"}

def save_cfg(cfg):
    with open(CFG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)

# Create default config if not exists
if not os.path.exists(CFG_PATH):
    # Try to read Hermes config for fallback
    hermes_key = ""
    try:
        env_path = os.path.expanduser("~/.hermes/.env")
        with open(env_path) as f:
            for line in f:
                m = re.match(r'DEEPSEEK_API_KEY=(.+)', line.strip())
                if m: hermes_key = m.group(1).strip("'\"")
    except:
        pass
    save_cfg({"llm_api_key": hermes_key, "llm_model": "deepseek-chat", "llm_base_url": "https://api.deepseek.com"})

# ── Models ──
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    reply: str
    session_id: str = ""

# ── Session history (in-memory, simple) ──
sessions = {}
MAX_HISTORY = 20

# ── Chat ──
@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    cfg = load_cfg()
    api_key = cfg.get("llm_api_key", "")
    model = cfg.get("llm_model", "deepseek-chat")
    base_url = cfg.get("llm_base_url", "https://api.deepseek.com")
    
    if not api_key:
        return ChatResponse(reply="⚠️ LLM API key not configured. Edit ~/.smart-ai/config.json", session_id=req.session_id)
    
    # Session management
    sid = req.session_id
    if sid not in sessions:
        sessions[sid] = []
    
    # Build messages
    msgs = [{"role": "system", "content": "You are Smart AI, a helpful AI assistant running as a Windows 11 desktop overlay. Respond concisely in the language the user uses. Be helpful, direct, and efficient."}]
    msgs.extend(sessions[sid][-MAX_HISTORY:])
    msgs.append({"role": "user", "content": req.message})
    
    try:
        payload = json.dumps({"model": model, "messages": msgs, "max_tokens": 1024}).encode()
        req_ = urllib.request.Request(base_url + "/v1/chat/completions", data=payload,
            headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
            method="POST")
        with urllib.request.urlopen(req_, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            reply = data["choices"][0]["message"]["content"]
        
        # Store in history
        sessions[sid].append({"role": "user", "content": req.message})
        sessions[sid].append({"role": "assistant", "content": reply})
        
        return ChatResponse(reply=reply, session_id=sid)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return ChatResponse(reply=f"⚠️ API error ({e.code}): {body[:200]}", session_id=sid)
    except Exception as e:
        return ChatResponse(reply=f"⚠️ Error: {str(e)[:200]}", session_id=sid)

# ── Health ──
@app.get("/health")
def health():
    return {"status": "ok", "service": "smart-ai", "version": "1.0.0"}

# ── Config endpoints ──
class ConfigUpdate(BaseModel):
    key: str
    value: str

@app.get("/api/v1/config")
def get_config():
    return load_cfg()

@app.post("/api/v1/config")
def set_config(cfg: ConfigUpdate):
    c = load_cfg()
    c[cfg.key] = cfg.value
    save_cfg(c)
    return {"ok": True}

@app.get("/api/v1/sessions")
def list_sessions():
    return {"sessions": list(sessions.keys()), "count": len(sessions)}

if __name__ == "__main__":
    port = int(os.environ.get("SMART_AI_PORT", 8765))
    print(f"Smart AI Server starting on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
