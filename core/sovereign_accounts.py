import json, time, hashlib
from pathlib import Path
ACCOUNTS_FILE = Path.home() / "PhoneServe/sovereign_accounts.json"
MAIL_DATA = Path.home() / "PhoneServe/mail_data.json"
def load_accounts():
    if not ACCOUNTS_FILE.exists():
        return {"users":[],"signups":[]}
    try:
        return json.loads(ACCOUNTS_FILE.read_text())
    except:
        return {"users":[],"signups":[]}
def save_accounts(data):
    ACCOUNTS_FILE.write_text(json.dumps(data, indent=2))
def signup(username, display_name, password):
    username = username.lower().strip()
    if not username: return {"ok":False,"error":"username required"}
    data = load_accounts()
    if any(u['username']==username for u in data['users']): return {"ok":False,"error":"Username taken"}
    if any(s['username']==username for s in data['signups']): return {"ok":False,"error":"Already requested"}
    pw = hashlib.sha256(password.encode()).hexdigest()
    entry = {"username":username,"display_name":display_name,"email":f"{username}@edgetech-knowledgey.fwh.is","password_hash":pw,"timestamp":time.time(),"status":"pending"}
    data['signups'].append(entry)
    save_accounts(data)
    return {"ok":True,"email":entry['email']}
def approve(username):
    data = load_accounts()
    s = next((x for x in data['signups'] if x['username']==username), None)
    if not s: return {"ok":False,"error":"Not found"}
    user = {"username":s['username'],"display_name":s['display_name'],"email":s['email'],"password_hash":s['password_hash'],"created":time.time(),"storage_used":0,"storage_limit":1073741824,"tier":"sovereign"}
    data['users'].append(user)
    data['signups']=[x for x in data['signups'] if x['username']!=username]
    save_accounts(data)
    try:
        md = json.loads(MAIL_DATA.read_text()) if MAIL_DATA.exists() else {"inbox":[]}
        welcome = {"id":f"welcome-{username}-{int(time.time())}","from_name":"ETK System","from_addr":"system@edgetech-knowledgey.fwh.is","to":user['email'],"subject":f"Welcome {user['display_name']}!","body":f"Mailbox {user['email']} LIVE on ETK-3C6FF9C4","timestamp":time.time(),"read":False,"folder":"inbox"}
        md.setdefault('inbox',[]).insert(0,welcome)
        MAIL_DATA.write_text(json.dumps(md,indent=2))
    except Exception as e:
        print(e)
    return {"ok":True,"user":user}
def list_all():
    return load_accounts()
