"""
ETK Mail Server v1.0
Edge Tech Knowledgey // Sovereign Email Infrastructure
Runs on your Moto G Stylus 5G alongside PhoneServe mesh gateway

Ports:
  SMTP : 8025  (send/receive mail)
  IMAP : 8143  (read mail)
  API  : 8585  (browser frontend talks here)

Run: python3 etk_mail_server.py
"""

import asyncio
import json
import os
import hashlib
import time
import uuid
import logging
import base64
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.parser import Parser
from email.policy import default as email_policy

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [ETK-MAIL] %(levelname)s: %(message)s'
)
logger = logging.getLogger('ETK-MAIL')

# ── CONFIG ──────────────────────────────────────────────────
CONFIG = {
    'domain':      'edgetech-knowledgey.fwh.is',
    'owner_email': 'david@edgetech-knowledgey.fwh.is',
    'owner_name':  'David Ingalls',
    'owner_role':  'Chief Architect',
    'smtp_port':   8025,
    'imap_port':   8143,
    'api_port':    8585,
    'mailbox_dir': './etk_mailbox',
    'max_emails':  10000,
}

# ── MAIL STORE ──────────────────────────────────────────────
class MailStore:
    def __init__(self):
        self.inbox   = []
        self.sent    = []
        self.drafts  = []
        self.trash   = []
        self.folders = {
            'inbox':  self.inbox,
            'sent':   self.sent,
            'drafts': self.drafts,
            'trash':  self.trash,
        }
        os.makedirs(CONFIG['mailbox_dir'], exist_ok=True)
        self._load()
        self._seed_welcome()

    def _load(self):
        for folder in self.folders:
            path = f"{CONFIG['mailbox_dir']}/{folder}.json"
            if os.path.exists(path):
                try:
                    with open(path) as f:
                        self.folders[folder][:] = json.load(f)
                    logger.info(f"Loaded {len(self.folders[folder])} emails from {folder}")
                except Exception as e:
                    logger.error(f"Failed to load {folder}: {e}")

    def _save(self, folder):
        path = f"{CONFIG['mailbox_dir']}/{folder}.json"
        try:
            with open(path, 'w') as f:
                json.dump(self.folders[folder], f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save {folder}: {e}")

    def _seed_welcome(self):
        if not self.inbox:
            self.deliver({
                'id':        str(uuid.uuid4()),
                'from_name': 'ETK Mail Server',
                'from_addr': f"server@{CONFIG['domain']}",
                'to':        CONFIG['owner_email'],
                'subject':   'Welcome to ETK Sovereign Mail',
                'body':      f"""Welcome, {CONFIG['owner_name']}.

Your sovereign ETK mail server is now running on your device.

Account  : {CONFIG['owner_email']}
Role     : {CONFIG['owner_role']} · ADMINISTRATOR
Domain   : {CONFIG['domain']}
Server   : PhoneServe Mesh Node

This email server runs entirely on your Moto G Stylus 5G.
No third parties. No data sharing. Fully sovereign.

SMTP Port : {CONFIG['smtp_port']}
IMAP Port : {CONFIG['imap_port']}
API  Port : {CONFIG['api_port']}

— ETK Mail Server v1.0
Edge Tech Knowledgey""",
                'timestamp': datetime.now().isoformat(),
                'read':      False,
                'starred':   True,
                'label':     'system',
            })

    def deliver(self, email):
        """Deliver incoming email to inbox."""
        if 'id' not in email:
            email['id'] = str(uuid.uuid4())
        if 'timestamp' not in email:
            email['timestamp'] = datetime.now().isoformat()
        email['read'] = False
        self.inbox.insert(0, email)
        self._save('inbox')
        logger.info(f"📥 Delivered: {email['subject'][:40]} from {email['from_addr']}")
        return email['id']

    def send(self, email):
        """Store outgoing email."""
        email['id']        = str(uuid.uuid4())
        email['timestamp'] = datetime.now().isoformat()
        email['read']      = True
        self.sent.insert(0, email)
        self._save('sent')
        logger.info(f"📤 Sent: {email['subject'][:40]} to {email['to']}")
        return email['id']

    def get_folder(self, folder):
        return self.folders.get(folder, [])

    def mark_read(self, email_id):
        for folder in self.folders.values():
            for e in folder:
                if e['id'] == email_id:
                    e['read'] = True
                    return True
        return False

    def toggle_star(self, email_id):
        for folder in self.folders.values():
            for e in folder:
                if e['id'] == email_id:
                    e['starred'] = not e.get('starred', False)
                    return e['starred']
        return False

    def delete(self, email_id, from_folder='inbox'):
        folder = self.folders.get(from_folder, [])
        email  = next((e for e in folder if e['id'] == email_id), None)
        if email:
            folder.remove(email)
            self.trash.insert(0, email)
            self._save(from_folder)
            self._save('trash')
            return True
        return False

    def stats(self):
        return {
            'inbox_total':  len(self.inbox),
            'inbox_unread': sum(1 for e in self.inbox if not e.get('read')),
            'sent_total':   len(self.sent),
            'drafts_total': len(self.drafts),
            'trash_total':  len(self.trash),
            'domain':       CONFIG['domain'],
            'owner':        CONFIG['owner_email'],
            'role':         CONFIG['owner_role'],
            'uptime':       int(time.time() - _START_TIME),
        }

_START_TIME = time.time()
store = MailStore()

# ── SMTP SERVER ─────────────────────────────────────────────
class SMTPSession:
    def __init__(self, reader, writer):
        self.reader  = reader
        self.writer  = writer
        self.peer    = writer.get_extra_info('peername')
        self.mail_from   = None
        self.rcpt_to     = []
        self.data_mode   = False
        self.data_buffer = []

    async def send(self, msg):
        self.writer.write((msg + '\r\n').encode())
        await self.writer.drain()

    async def handle(self):
        await self.send(f"220 {CONFIG['domain']} ETK-SMTP-Server Ready")
        logger.info(f"SMTP connection from {self.peer}")
        try:
            while True:
                line = await self.reader.readline()
                if not line:
                    break
                text = line.decode('utf-8', errors='ignore').strip()
                if self.data_mode:
                    if text == '.':
                        self.data_mode = False
                        await self._process_data()
                    else:
                        self.data_buffer.append(text.lstrip('.') if text.startswith('..') else text)
                else:
                    await self._handle_command(text)
        except Exception as e:
            logger.debug(f"SMTP session error: {e}")
        finally:
            self.writer.close()

    async def _handle_command(self, text):
        upper = text.upper()
        if upper.startswith('EHLO') or upper.startswith('HELO'):
            await self.send(f"250-{CONFIG['domain']} Hello")
            await self.send("250-SIZE 52428800")
            await self.send("250 OK")
        elif upper.startswith('MAIL FROM:'):
            self.mail_from = text[10:].strip().strip('<>')
            await self.send("250 OK")
        elif upper.startswith('RCPT TO:'):
            rcpt = text[8:].strip().strip('<>')
            self.rcpt_to.append(rcpt)
            await self.send("250 OK")
        elif upper == 'DATA':
            await self.send("354 Start input, end with <CRLF>.<CRLF>")
            self.data_mode   = True
            self.data_buffer = []
        elif upper == 'QUIT':
            await self.send("221 Bye")
        elif upper == 'RSET':
            self.mail_from = None; self.rcpt_to = []; self.data_buffer = []
            await self.send("250 OK")
        elif upper.startswith('NOOP'):
            await self.send("250 OK")
        else:
            await self.send("500 Unknown command")

    async def _process_data(self):
        raw  = '\n'.join(self.data_buffer)
        try:
            parser  = Parser(policy=email_policy)
            msg_obj = parser.parsestr(raw)
            subject = str(msg_obj.get('Subject', '(no subject)'))
            body    = ''
            if msg_obj.is_multipart():
                for part in msg_obj.walk():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
            else:
                payload = msg_obj.get_payload(decode=True)
                body = payload.decode('utf-8', errors='ignore') if payload else msg_obj.get_payload()
        except Exception:
            subject = '(no subject)'
            body    = raw[:2000]

        for rcpt in self.rcpt_to:
            if CONFIG['domain'] in rcpt:
                store.deliver({
                    'from_name': self.mail_from.split('@')[0] if self.mail_from else 'Unknown',
                    'from_addr': self.mail_from or 'unknown@unknown',
                    'to':        rcpt,
                    'subject':   subject,
                    'body':      body or raw[:2000],
                    'label':     '',
                })
        await self.send("250 Message accepted")
        logger.info(f"SMTP: accepted message from {self.mail_from}")
        self.mail_from = None; self.rcpt_to = []; self.data_buffer = []

async def smtp_handler(reader, writer):
    session = SMTPSession(reader, writer)
    await session.handle()

# ── API SERVER (browser frontend) ───────────────────────────
CORS = (
    "Access-Control-Allow-Origin: *\r\n"
    "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
    "Access-Control-Allow-Headers: Content-Type\r\n"
)

async def api_handler(reader, writer):
    try:
        raw = await reader.read(16384)
        req = raw.decode('utf-8', errors='ignore')
        lines    = req.split('\r\n')
        req_line = lines[0].split(' ')
        method   = req_line[0] if req_line else 'GET'
        path     = req_line[1] if len(req_line) > 1 else '/'

        # CORS preflight
        if method == 'OPTIONS':
            resp = f"HTTP/1.1 204 No Content\r\n{CORS}\r\n"
            writer.write(resp.encode()); await writer.drain()
            writer.close(); return

        # Parse body
        body_text = ''
        if '\r\n\r\n' in req:
            body_text = req.split('\r\n\r\n', 1)[1]
        body_json = {}
        if body_text.strip():
            try: body_json = json.loads(body_text)
            except: pass

        # Route
        if path == '/api/stats':
            data = store.stats()
        elif path == '/api/folder' and method == 'POST':
            folder = body_json.get('folder', 'inbox')
            data   = {'emails': store.get_folder(folder), 'folder': folder}
        elif path == '/api/read' and method == 'POST':
            eid  = body_json.get('id')
            data = {'ok': store.mark_read(eid)}
        elif path == '/api/star' and method == 'POST':
            eid     = body_json.get('id')
            starred = store.toggle_star(eid)
            data    = {'ok': True, 'starred': starred}
        elif path == '/api/delete' and method == 'POST':
            eid    = body_json.get('id')
            folder = body_json.get('folder', 'inbox')
            data   = {'ok': store.delete(eid, folder)}
        elif path == '/api/send' and method == 'POST':
            email = {
                'from_name': CONFIG['owner_name'],
                'from_addr': CONFIG['owner_email'],
                'to':        body_json.get('to', ''),
                'subject':   body_json.get('subject', '(no subject)'),
                'body':      body_json.get('body', ''),
                'label':     '',
            }
            msg_id = store.send(email)
            # If recipient is on same domain, deliver to inbox too
            if CONFIG['domain'] in email['to']:
                store.deliver({**email, 'from_name': CONFIG['owner_name'],
                    'from_addr': CONFIG['owner_email']})
            data = {'ok': True, 'id': msg_id}
            logger.info(f"API SEND → {email['to']}: {email['subject'][:30]}")
        elif path == '/api/receive' and method == 'POST':
            # Receive email posted from external source
            email = body_json
            msg_id = store.deliver(email)
            data = {'ok': True, 'id': msg_id}
        else:
            data = {'error': 'Unknown endpoint', 'path': path}

        resp_body = json.dumps(data)
        response  = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: application/json\r\n"
            f"Content-Length: {len(resp_body)}\r\n"
            f"{CORS}\r\n"
            f"{resp_body}"
        )
        writer.write(response.encode())
        await writer.drain()
    except Exception as e:
        logger.error(f"API error: {e}")
    finally:
        try: writer.close()
        except: pass

# ── BOOT ────────────────────────────────────────────────────
async def main():
    smtp_server = await asyncio.start_server(smtp_handler, '0.0.0.0', CONFIG['smtp_port'])
    api_server  = await asyncio.start_server(api_handler,  '0.0.0.0', CONFIG['api_port'])

    logger.info("═══════════════════════════════════════════════════")
    logger.info("  ETK Mail Server v1.0")
    logger.info(f"  Domain  : {CONFIG['domain']}")
    logger.info(f"  Owner   : {CONFIG['owner_email']} · {CONFIG['owner_role']}")
    logger.info(f"  SMTP    : 0.0.0.0:{CONFIG['smtp_port']}")
    logger.info(f"  API     : 0.0.0.0:{CONFIG['api_port']}")
    logger.info(f"  Mailbox : {CONFIG['mailbox_dir']}/")
    logger.info("═══════════════════════════════════════════════════")
    logger.info("  ETK Sovereign Mail — running on your device")

    async with smtp_server, api_server:
        await asyncio.gather(
            smtp_server.serve_forever(),
            api_server.serve_forever()
        )

if __name__ == '__main__':
    asyncio.run(main())
