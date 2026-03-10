#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║          HagePe Deface Generator  v4.0  —  BEAST EDITION        ║
║          Developer  : CyberKallan  (GitHub: CyberKallan)        ║
║          Recoded by : Hypervenom   (Instagram: @imarjunarz)     ║
╚══════════════════════════════════════════════════════════════════╝

  Run:  python3 hagepev4.py
  Req:  Python 3.9+  (zero third-party dependencies)

  Features:
    ✔  YouTube / MP3 / SoundCloud auto-embed fixer
    ✔  Live Preview Server  → localhost:7070
    ✔  Animated Download Page Server → localhost:8080
    ✔  Mobile-First Responsive Mode
    ✔  Page Encryption (SHA-256 password gate)
    ✔  10 Themes × 6 Fonts × full animation engine
    ✔  Profile auto-save / reload
"""

import os, sys, re, time, json, random, base64, hashlib
import threading, webbrowser, datetime, urllib.request, urllib.error, urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 1 — TERMINAL UI
# ══════════════════════════════════════════════════════════════════════════════

R   = "\033[0m"
BLD = "\033[1m"
DIM = "\033[2m"
CYN = "\033[96m"
GRN = "\033[92m"
RED = "\033[91m"
YLW = "\033[93m"
MGT = "\033[95m"
BLU = "\033[94m"
WHT = "\033[97m"

def clr():
    os.system("cls" if os.name == "nt" else "clear")

def typewrite(text, delay=0.016, color=""):
    for ch in text:
        sys.stdout.write(color + ch + R)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def progress(label, color=CYN, width=38):
    print(f"\n  {DIM}{color}{label}...{R}")
    val = 0
    while val < 100:
        val = min(val + random.randint(3, 9), 100)
        filled = int(width * val / 100)
        bar = "█" * filled + "░" * (width - filled)
        sys.stdout.write(f"\r  {color}[{bar}] {val:3d}%{R}  ")
        sys.stdout.flush()
        time.sleep(random.uniform(0.01, 0.04))
    print(f"  {GRN}✔{R}")

def ask(prompt, default="", color=YLW):
    val = input(f"  {color}{BLD}{prompt}{R}  {DIM}[{default}]{R} : ").strip()
    return val if val else default

def ask_choice(prompt, valid_keys, default="1", color=GRN):
    val = input(f"\n  {color}{BLD}❯ {prompt}: {R}").strip()
    return val if val in valid_keys else default

def ask_yn(prompt, default=False):
    d = "Y/n" if default else "y/N"
    val = input(f"  {BLU}{BLD}{prompt}{R}  {DIM}[{d}]{R} : ").strip().lower()
    if val in ("y", "yes"): return True
    if val in ("n", "no"):  return False
    return default

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 2 — CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

CONFIG_DEFAULTS = {
    "title": "Hacked", "heading": "YOU HAVE BEEN PWNED", "subheading": "",
    "imagelink": "", "bgimage": "", "message": "This system has been compromised.",
    "textcolor": "#ffffff", "contact_email": "", "raw_media": "",
    "theme": "1", "font": "1", "mobile": False,
    "encrypt": False, "password": "", "filename": "index.html",
}

THEMES = {
    "1":  ("Hacker Green",   "#00ff41", "#080808"),
    "2":  ("Matrix Rain",    "#39ff14", "#001100"),
    "3":  ("Dark Glitch",    "#ff003c", "#0a0010"),
    "4":  ("Cyberpunk Neon", "#ffe600", "#0d0020"),
    "5":  ("Retro Terminal", "#ff8c00", "#140800"),
    "6":  ("Minimal Dark",   "#e0e0e0", "#111111"),
    "7":  ("Blood Red",      "#ff2020", "#0d0000"),
    "8":  ("Ice Blue",       "#00cfff", "#00101a"),
    "9":  ("Ghost White",    "#f5f5f5", "#1a1a1a"),
    "10": ("Toxic Lime",     "#aaff00", "#061000"),
}

FONTS = {
    "1": "Orbitron",
    "2": "Share Tech Mono",
    "3": "VT323",
    "4": "Major Mono Display",
    "5": "Courier Prime",
    "6": "Nova Mono",
}

THEME_TERM_COLORS = {
    "1": GRN, "2": GRN,  "3": RED, "4": YLW,
    "5": YLW, "6": WHT,  "7": RED, "8": CYN,
    "9": WHT, "10": GRN,
}

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 3 — MEDIA RESOLVER  (YouTube / SoundCloud / MP3)
# ══════════════════════════════════════════════════════════════════════════════

_YT_PATTERNS = [
    r"(?:youtube\.com/watch\?(?:.*&)?v=)([A-Za-z0-9_\-]{11})",
    r"(?:youtu\.be/)([A-Za-z0-9_\-]{11})",
    r"(?:youtube\.com/shorts/)([A-Za-z0-9_\-]{11})",
    r"(?:youtube\.com/embed/)([A-Za-z0-9_\-]{11})",
]
_AUDIO_EXTS = (".mp3", ".ogg", ".wav", ".aac", ".flac", ".opus")

def _yt_id(url):
    for pat in _YT_PATTERNS:
        m = re.search(pat, url)
        if m: return m.group(1)
    return None

def resolve_media(url):
    """
    Returns (media_type, embed_html).
    Types: 'youtube' | 'soundcloud' | 'mp3' | 'unknown' | 'none'
    """
    if not url or not url.strip():
        return ("none", "")
    url = url.strip()

    # ── YouTube ──
    vid = _yt_id(url)
    if vid:
        embed = (
            f'<div id="yt-wrap" style="position:fixed;bottom:20px;right:20px;'
            f'z-index:9999;width:1px;height:1px;opacity:0;pointer-events:none;">'
            f'<iframe id="yt-frame" width="1" height="1" '
            f'src="https://www.youtube.com/embed/{vid}?autoplay=1&loop=1'
            f'&playlist={vid}&mute=0&controls=0&modestbranding=1&rel=0" '
            f'frameborder="0" allow="autoplay;encrypted-media" allowfullscreen>'
            f'</iframe></div>'
            f'<script>document.addEventListener("click",function(){{'
            f'var f=document.getElementById("yt-frame");if(f)f.src=f.src;'
            f'}},{{once:true}});</script>'
        )
        return ("youtube", embed)

    # ── SoundCloud ──
    if "soundcloud.com" in url.lower():
        enc = url.replace("&", "%26")
        embed = (
            f'<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" '
            f'src="https://w.soundcloud.com/player/?url={enc}'
            f'&color=%2300ff41&auto_play=true&hide_related=true'
            f'&show_comments=false&show_user=false&show_teaser=false" '
            f'style="position:fixed;bottom:-200px;left:0;z-index:9998;'
            f'opacity:0;pointer-events:none;"></iframe>'
        )
        return ("soundcloud", embed)

    # ── Direct audio ──
    if any(url.split("?")[0].lower().endswith(ext) for ext in _AUDIO_EXTS):
        embed = (
            f'<audio id="bgaudio" src="{url}" loop preload="auto" style="display:none;"></audio>'
            f'<script>document.addEventListener("click",function(){{'
            f'var a=document.getElementById("bgaudio");'
            f'if(a)a.play().catch(function(){{}});'
            f'}},{{once:true}});</script>'
        )
        return ("mp3", embed)

    # ── Unknown — attempt audio ──
    embed = (
        f'<audio id="bgaudio" src="{url}" loop preload="auto" style="display:none;"></audio>'
        f'<script>document.addEventListener("click",function(){{'
        f'var a=document.getElementById("bgaudio");'
        f'if(a)a.play().catch(function(){{}});'
        f'}},{{once:true}});</script>'
    )
    return ("unknown", embed)

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 4 — HTML BUILDER
# ══════════════════════════════════════════════════════════════════════════════

_SCANLINE_CSS = """
  #overlay::after{content:'';position:absolute;inset:0;
    background:repeating-linear-gradient(to bottom,transparent 0,transparent 2px,
      rgba(0,0,0,.15) 2px,rgba(0,0,0,.15) 4px);
    pointer-events:none;animation:scanroll 10s linear infinite;}
  @keyframes scanroll{from{background-position:0 0}to{background-position:0 100%}}
"""
_GLITCH_CSS = """
  @keyframes glitch-txt{
    0%,90%,100%{text-shadow:0 0 16px var(--acc);transform:none}
    91%{text-shadow:-4px 0 #ff003c,4px 0 #00ffff;transform:skewX(-5deg)}
    93%{text-shadow:4px 0 #ff00ff,-4px 0 #00ff00;transform:skewX(5deg) scaleX(1.02)}
    95%{text-shadow:0 0 16px var(--acc);transform:none}}
"""
_NEON_CSS = """
  @keyframes neon-flicker{
    0%,18%,20%,22%,52%,54%,64%,100%{text-shadow:0 0 16px var(--acc),0 0 36px var(--acc);opacity:1}
    19%,21%,53%,63%{opacity:.6;text-shadow:none}}
"""
_MOBILE_CSS = """
  @media(max-width:600px){
    h1{font-size:clamp(1.1rem,7vw,1.8rem)!important;letter-spacing:.06em!important;}
    #message-box{padding:16px 14px!important;font-size:.82rem!important;}
    #logo{width:80px!important;height:80px!important;}
    .contact-btn{padding:8px 16px!important;font-size:.72rem!important;}
    #main{padding:24px 14px!important;gap:18px!important;}}
  @media(hover:none){.contact-btn:hover{transform:none!important;}}
"""
_MATRIX_JS = """
(function(){
  var c=document.getElementById('bgCanvas'),ctx=c.getContext('2d');
  function rs(){c.width=window.innerWidth;c.height=window.innerHeight;}rs();
  window.addEventListener('resize',rs);
  var cols=Math.floor(c.width/18),drops=Array(cols).fill(1);
  var chars='01アイウカキクサシスタチナニハヒフマミムラリルワヲン';
  var acc=getComputedStyle(document.documentElement).getPropertyValue('--acc').trim();
  function draw(){
    ctx.fillStyle='rgba(0,0,0,0.06)';ctx.fillRect(0,0,c.width,c.height);
    ctx.fillStyle=acc;ctx.font='14px monospace';
    drops.forEach(function(y,i){
      var ch=chars[Math.floor(Math.random()*chars.length)];
      ctx.fillText(ch,i*18,y*18);
      if(y*18>c.height&&Math.random()>.975)drops[i]=0;drops[i]++;});
  }
  setInterval(draw,45);
})();
"""
_PARTICLE_JS = """
(function(){
  var c=document.getElementById('bgCanvas'),ctx=c.getContext('2d');
  function rs(){c.width=window.innerWidth;c.height=window.innerHeight;}rs();
  window.addEventListener('resize',rs);
  var acc=getComputedStyle(document.documentElement).getPropertyValue('--acc').trim();
  var pts=Array.from({length:90},function(){
    return{x:Math.random()*c.width,y:Math.random()*c.height,
           vx:(Math.random()-.5)*.5,vy:(Math.random()-.5)*.5,r:Math.random()*1.6+.3};});
  function draw(){
    ctx.clearRect(0,0,c.width,c.height);
    pts.forEach(function(p){
      ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fillStyle=acc;ctx.fill();
      p.x+=p.vx;p.y+=p.vy;
      if(p.x<0)p.x=c.width;if(p.x>c.width)p.x=0;
      if(p.y<0)p.y=c.height;if(p.y>c.height)p.y=0;});
    for(var i=0;i<pts.length;i++){
      for(var j=i+1;j<pts.length;j++){
        var dx=pts[i].x-pts[j].x,dy=pts[i].y-pts[j].y,d=Math.sqrt(dx*dx+dy*dy);
        if(d<120){ctx.beginPath();ctx.moveTo(pts[i].x,pts[i].y);
          ctx.lineTo(pts[j].x,pts[j].y);ctx.strokeStyle=acc;
          ctx.globalAlpha=(1-d/120)*.18;ctx.lineWidth=.6;ctx.stroke();ctx.globalAlpha=1;}}}
  }
  setInterval(draw,28);
})();
"""

def _theme_flags(tid):
    return {
        "1":  (False, False, False, True),
        "2":  (True,  False, False, False),
        "3":  (False, True,  False, False),
        "4":  (False, False, True,  False),
        "5":  (False, False, False, True),
        "6":  (False, False, False, False),
        "7":  (False, True,  False, False),
        "8":  (False, False, True,  False),
        "9":  (False, False, False, False),
        "10": (True,  False, False, False),
    }.get(tid, (False, False, False, False))
    # returns (matrix, glitch, neon_flicker, scanline)

def build_html(cfg):
    tid  = cfg.get("theme", "1")
    tname, accent, bgcol = THEMES.get(tid, THEMES["1"])
    font = FONTS.get(cfg.get("font", "1"), "Orbitron")
    tc   = cfg.get("textcolor", "#ffffff")
    ts   = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    has_matrix, has_glitch, has_neon, has_scan = _theme_flags(tid)

    h1anim = ("animation:glitch-txt 2.5s infinite;" if has_glitch else
              "animation:neon-flicker 3s infinite;" if has_neon else
              "animation:glow-pulse 2.5s ease-in-out infinite;")

    sub_html   = f'<p id="subhead">{cfg["subheading"]}</p>' if cfg.get("subheading") else ""
    email_btn  = f'<a class="contact-btn" href="mailto:{cfg["contact_email"]}">✉ Contact</a>' if cfg.get("contact_email") else ""
    media_html = cfg.get("media_embed", "")
    bg_css     = f"url('{cfg['bgimage']}') no-repeat center center fixed" if cfg.get("bgimage") else "var(--bg)"
    logo_html  = (f'<img id="logo" src="{cfg["imagelink"]}" alt="Logo" '
                  f'onerror="this.style.display=\'none\'"/>') if cfg.get("imagelink") else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>{cfg.get('title','Hacked')}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family={font.replace(' ','+')}&display=swap" rel="stylesheet"/>
  <style>
    :root{{--acc:{accent};--bg:{bgcol};--font:'{font}',monospace;}}
    *,*::before,*::after{{margin:0;padding:0;box-sizing:border-box;}}
    body{{background:{bg_css};background-size:cover;background-color:var(--bg);
         font-family:var(--font);color:{tc};min-height:100vh;
         overflow-x:hidden;cursor:crosshair;}}
    #overlay{{position:fixed;inset:0;background:rgba(0,0,0,.65);
              backdrop-filter:blur(3px);z-index:0;}}
    {_SCANLINE_CSS if has_scan else ""}
    #bgCanvas{{position:fixed;inset:0;z-index:1;pointer-events:none;opacity:.4;}}
    #main{{position:relative;z-index:10;min-height:100vh;display:flex;
           flex-direction:column;align-items:center;justify-content:center;
           padding:48px 20px;gap:26px;}}
    #logo{{width:clamp(80px,16vw,200px);height:clamp(80px,16vw,200px);border-radius:50%;
           object-fit:cover;border:2px solid var(--acc);
           box-shadow:0 0 24px var(--acc),0 0 60px rgba(0,0,0,.5);
           animation:pulse-ring 2.6s ease-in-out infinite;}}
    @keyframes pulse-ring{{
      0%,100%{{box-shadow:0 0 16px var(--acc),0 0 40px rgba(0,0,0,.4);}}
      50%{{box-shadow:0 0 48px var(--acc),0 0 100px var(--acc);}}}}
    h1{{font-size:clamp(1.4rem,4.5vw,3rem);letter-spacing:.14em;text-transform:uppercase;
        color:var(--acc);text-shadow:0 0 16px var(--acc),0 0 40px var(--acc);
        {h1anim} line-height:1.2;}}
    @keyframes glow-pulse{{
      0%,100%{{text-shadow:0 0 14px var(--acc);}}
      50%{{text-shadow:0 0 40px var(--acc),0 0 80px var(--acc);}}}}
    {_GLITCH_CSS if has_glitch else ""}
    {_NEON_CSS   if has_neon   else ""}
    #subhead{{font-size:clamp(.8rem,2vw,1.1rem);letter-spacing:.2em;
              text-transform:uppercase;opacity:.6;margin-top:-8px;}}
    .divider{{width:min(540px,88vw);height:1px;
              background:linear-gradient(90deg,transparent,var(--acc),transparent);opacity:.6;}}
    #message-box{{max-width:min(720px,92vw);background:rgba(0,0,0,.58);
      border:1px solid var(--acc);border-radius:8px;padding:28px 34px;
      font-size:clamp(.84rem,2.1vw,1.05rem);line-height:1.95;letter-spacing:.04em;
      box-shadow:inset 0 0 28px rgba(0,0,0,.4),0 0 22px var(--acc);
      animation:fadein 1.2s ease both;}}
    @keyframes fadein{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:none}}}}
    #message-box::after{{content:"▮";color:var(--acc);
      animation:blink 1s step-end infinite;margin-left:4px;}}
    @keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:0}}}}
    #theme-badge{{font-size:.65rem;letter-spacing:.22em;text-transform:uppercase;
      color:var(--acc);opacity:.5;border:1px solid var(--acc);
      padding:3px 14px;border-radius:20px;}}
    #contacts{{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;}}
    .contact-btn{{font-family:var(--font);font-size:.76rem;letter-spacing:.16em;
      text-transform:uppercase;color:var(--bg);background:var(--acc);
      border:none;padding:10px 24px;border-radius:3px;cursor:pointer;
      text-decoration:none;transition:transform .15s,box-shadow .15s;
      box-shadow:0 0 14px var(--acc);}}
    .contact-btn:hover{{transform:translateY(-2px) scale(1.05);
      box-shadow:0 0 30px var(--acc),0 0 60px var(--acc);}}
    .spark{{position:fixed;width:3px;height:3px;background:var(--acc);
      border-radius:50%;pointer-events:none;z-index:999;
      animation:sparkfly var(--dur,1s) ease-out forwards;}}
    @keyframes sparkfly{{
      0%{{opacity:1;transform:translate(0,0) scale(1.2);}}
      100%{{opacity:0;transform:translate(var(--tx,40px),var(--ty,-60px)) scale(0);}}}}
    footer{{font-size:.64rem;opacity:.28;letter-spacing:.1em;text-align:center;}}
    {_MOBILE_CSS if cfg.get("mobile") else ""}
  </style>
</head>
<body>
<div id="overlay"></div>
<canvas id="bgCanvas"></canvas>
<div id="main">
  {logo_html}
  <span id="theme-badge">{tname}</span>
  <h1 id="heading">{cfg.get('heading','')}</h1>
  {sub_html}
  <div class="divider"></div>
  <div id="message-box">{cfg.get('message','')}</div>
  <div class="divider"></div>
  <div id="contacts">{email_btn}</div>
  <footer>HagePe v4.0 &nbsp;|&nbsp; {ts} &nbsp;|&nbsp; {tname} &nbsp;|&nbsp; Dev: CyberKallan &nbsp;|&nbsp; Recoded by: Hypervenom</footer>
</div>
{media_html}
<script>
{_MATRIX_JS if has_matrix else _PARTICLE_JS}
(function(){{
  var el=document.getElementById('heading'),txt=el.textContent;
  el.textContent='';var i=0;
  var iv=setInterval(function(){{el.textContent+=txt[i++];if(i>=txt.length)clearInterval(iv);}},60);
}})();
document.addEventListener('click',function(e){{
  for(var i=0;i<16;i++){{
    var s=document.createElement('div');s.className='spark';
    var a=Math.random()*Math.PI*2,d=30+Math.random()*80;
    s.style.setProperty('--tx',Math.cos(a)*d+'px');
    s.style.setProperty('--ty',Math.sin(a)*d+'px');
    s.style.setProperty('--dur',(0.5+Math.random()*.9)+'s');
    s.style.left=e.clientX+'px';s.style.top=e.clientY+'px';
    document.body.appendChild(s);
    s.addEventListener('animationend',function(){{s.remove();}});
  }}
}});
</script>
</body>
</html>"""

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 5 — ENCRYPTION WRAPPER
# ══════════════════════════════════════════════════════════════════════════════

def apply_encryption(html, password):
    key     = hashlib.sha256(password.encode()).hexdigest()
    encoded = base64.b64encode(html.encode("utf-8")).decode()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>403 Forbidden</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#080808;font-family:'Courier New',monospace;
      display:flex;align-items:center;justify-content:center;
      min-height:100vh;color:#00ff41;}}
.gate{{text-align:center;padding:40px;border:1px solid #00ff41;
       box-shadow:0 0 30px #00ff41;max-width:400px;width:90%;}}
h2{{font-size:1.4rem;margin-bottom:8px;letter-spacing:.15em;text-shadow:0 0 12px #00ff41;}}
p{{font-size:.75rem;opacity:.5;margin-bottom:28px;}}
input{{width:100%;padding:12px;background:transparent;border:1px solid #00ff41;
       color:#00ff41;font-family:inherit;font-size:1rem;text-align:center;
       outline:none;letter-spacing:.2em;}}
input:focus{{box-shadow:0 0 12px #00ff41;}}
button{{margin-top:16px;width:100%;padding:12px;background:#00ff41;
        color:#080808;font-family:inherit;font-size:.9rem;font-weight:bold;
        border:none;cursor:pointer;letter-spacing:.2em;transition:box-shadow .2s;}}
button:hover{{box-shadow:0 0 20px #00ff41;}}
#err{{color:#ff003c;font-size:.8rem;margin-top:12px;min-height:18px;}}
</style>
</head>
<body>
<div class="gate">
  <h2>🔐 ACCESS DENIED</h2>
  <p>This page is protected. Enter the key to proceed.</p>
  <input type="password" id="pwd" placeholder="_ _ _ _ _ _ _ _" autofocus/>
  <button onclick="unlock()">AUTHENTICATE</button>
  <div id="err"></div>
</div>
<script>
var _enc="{encoded}",_key="{key}";
function unlock(){{
  var pwd=document.getElementById('pwd').value;
  crypto.subtle.digest('SHA-256',new TextEncoder().encode(pwd)).then(function(buf){{
    var hex=Array.from(new Uint8Array(buf)).map(function(b){{return b.toString(16).padStart(2,'0')}}).join('');
    if(hex===_key){{var d=atob(_enc);document.open();document.write(d);document.close();}}
    else{{document.getElementById('err').textContent='⚠ Incorrect key. Access denied.';
          document.getElementById('pwd').value='';}}
  }});
}}
document.getElementById('pwd').addEventListener('keydown',function(e){{if(e.key==='Enter')unlock();}});
</script>
</body>
</html>"""

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 6 — LOCAL SERVERS  (Preview + Download)
# ══════════════════════════════════════════════════════════════════════════════

# ── Preview ────────────────────────────────────────────────────────────────────
class _PreviewHandler(BaseHTTPRequestHandler):
    filepath = ""
    def do_GET(self):
        try:
            with open(self.__class__.filepath, "rb") as f: data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers(); self.wfile.write(data)
        except Exception as e: self.send_error(500, str(e))
    def log_message(self, *a): pass

class PreviewServer:
    PORT = 7070
    def __init__(self, filepath):
        self.filepath = filepath
        _PreviewHandler.filepath = filepath
        self._srv = HTTPServer(("127.0.0.1", self.PORT), _PreviewHandler)
        self._t   = threading.Thread(target=self._srv.serve_forever, daemon=True)
    def start_and_open(self):
        self._t.start()
        url = f"http://localhost:{self.PORT}"
        print(f"\n  {GRN}✔ Preview → {YLW}{url}{R}")
        webbrowser.open(url)
    def stop(self):
        self._srv.shutdown()
        print(f"\n  {RED}⏹  Preview server stopped.{R}")

# ── Download ───────────────────────────────────────────────────────────────────
def _dl_page(filename, cfg):
    tname = THEMES.get(cfg.get("theme","1"), THEMES["1"])[0]
    fname = cfg.get("_filepath","")
    fsize = f"{os.path.getsize(fname):,} bytes" if fname and os.path.exists(fname) else "—"
    font  = FONTS.get(cfg.get("font","1"), "Orbitron")
    safe  = urllib.parse.quote(filename)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Download — {filename}</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet"/>
<style>
:root{{--g:#00ff41;--bg:#060a06;}}
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:var(--bg);font-family:'Share Tech Mono',monospace;color:var(--g);
      min-height:100vh;display:flex;align-items:center;justify-content:center;
      overflow:hidden;cursor:crosshair;}}
canvas{{position:fixed;inset:0;z-index:0;opacity:.3;}}
.wrap{{position:relative;z-index:10;width:min(540px,94vw);text-align:center;
       padding:48px 40px;border:1px solid var(--g);
       background:rgba(0,255,65,.03);backdrop-filter:blur(6px);
       box-shadow:0 0 60px rgba(0,255,65,.16);animation:appear .8s ease both;}}
@keyframes appear{{from{{opacity:0;transform:translateY(28px)}}to{{opacity:1;transform:none}}}}
.ring{{width:88px;height:88px;border-radius:50%;border:2px solid var(--g);
       display:flex;align-items:center;justify-content:center;margin:0 auto 28px;
       font-size:2.2rem;animation:rglow 3s ease-in-out infinite;}}
@keyframes rglow{{0%,100%{{box-shadow:0 0 18px var(--g);}}50%{{box-shadow:0 0 44px var(--g),0 0 80px var(--g);}}}}
h1{{font-family:'Orbitron',monospace;font-size:clamp(1rem,3.5vw,1.5rem);font-weight:900;
    letter-spacing:.14em;text-transform:uppercase;text-shadow:0 0 16px var(--g);
    margin-bottom:6px;animation:flkr 4s infinite;}}
@keyframes flkr{{0%,94%,100%{{opacity:1}}95%{{opacity:.4}}97%{{opacity:.9}}}}
.sub{{font-size:.7rem;opacity:.45;letter-spacing:.2em;margin-bottom:28px;}}
.meta{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:28px;text-align:left;}}
.mi{{background:rgba(0,255,65,.05);border:1px solid rgba(0,255,65,.18);padding:10px 14px;border-radius:4px;}}
.mi .lbl{{font-size:.58rem;opacity:.45;letter-spacing:.2em;text-transform:uppercase;}}
.mi .val{{font-size:.82rem;margin-top:4px;}}
.pb-wrap{{margin-bottom:24px;}}
.pb{{height:3px;background:rgba(0,255,65,.12);border-radius:2px;overflow:hidden;}}
.pf{{height:100%;background:var(--g);width:0%;box-shadow:0 0 8px var(--g);transition:width .05s;}}
.pl{{font-size:.62rem;opacity:.45;margin-top:6px;letter-spacing:.1em;}}
.dlbtn{{display:none;width:100%;padding:16px;background:var(--g);color:#060a06;
        font-family:'Orbitron',monospace;font-size:.82rem;font-weight:700;
        letter-spacing:.18em;text-transform:uppercase;text-decoration:none;
        border:none;cursor:pointer;border-radius:3px;box-shadow:0 0 18px var(--g);
        transition:transform .15s,box-shadow .15s;}}
.dlbtn:hover{{transform:scale(1.03);box-shadow:0 0 42px var(--g);}}
.credits{{margin-top:22px;font-size:.58rem;opacity:.28;letter-spacing:.12em;}}
.spark{{position:fixed;width:3px;height:3px;background:var(--g);border-radius:50%;
        pointer-events:none;z-index:999;animation:spk var(--d,.9s) ease-out forwards;}}
@keyframes spk{{0%{{opacity:1;transform:translate(0,0)}}100%{{opacity:0;transform:translate(var(--tx),var(--ty))}}}}
</style>
</head>
<body>
<canvas id="bg"></canvas>
<div class="wrap">
  <div class="ring">📄</div>
  <h1>Download Ready</h1>
  <p class="sub">Your deface page has been compiled</p>
  <div class="meta">
    <div class="mi"><div class="lbl">File</div><div class="val">{filename}</div></div>
    <div class="mi"><div class="lbl">Size</div><div class="val">{fsize}</div></div>
    <div class="mi"><div class="lbl">Theme</div><div class="val">{tname}</div></div>
    <div class="mi"><div class="lbl">Font</div><div class="val">{font}</div></div>
  </div>
  <div class="pb-wrap">
    <div class="pb"><div class="pf" id="pf"></div></div>
    <div class="pl" id="pl">Preparing file...</div>
  </div>
  <a class="dlbtn" id="dlbtn" href="/download/{safe}" download="{filename}">⬇ &nbsp; DOWNLOAD INDEX.HTML</a>
  <div class="credits">HagePe v4.0 &nbsp;|&nbsp; Developer: CyberKallan &nbsp;|&nbsp; Recoded by: Hypervenom</div>
</div>
<script>
(function(){{
  var c=document.getElementById('bg'),ctx=c.getContext('2d');
  c.width=window.innerWidth;c.height=window.innerHeight;
  window.addEventListener('resize',function(){{c.width=window.innerWidth;c.height=window.innerHeight;}});
  var cols=Math.floor(c.width/16),drops=Array(cols).fill(1);
  var chars='01アカサタナハ';
  function draw(){{ctx.fillStyle='rgba(0,0,0,.07)';ctx.fillRect(0,0,c.width,c.height);
    ctx.fillStyle='#00ff41';ctx.font='13px monospace';
    drops.forEach(function(y,i){{ctx.fillText(chars[Math.floor(Math.random()*chars.length)],i*16,y*16);
      if(y*16>c.height&&Math.random()>.975)drops[i]=0;drops[i]++;}});}}
  setInterval(draw,50);
}})();
(function(){{
  var pf=document.getElementById('pf'),pl=document.getElementById('pl');
  var msgs=['Compiling assets...','Verifying integrity...','Packaging file...','Ready!'];
  var val=0;
  var iv=setInterval(function(){{
    val=Math.min(val+Math.random()*8+2,100);
    pf.style.width=val+'%';
    pl.textContent=msgs[Math.min(Math.floor(val/26),msgs.length-1)];
    if(val>=100){{clearInterval(iv);document.getElementById('dlbtn').style.display='inline-block';}}
  }},80);
}})();
document.addEventListener('click',function(e){{
  for(var i=0;i<12;i++){{
    var s=document.createElement('div');s.className='spark';
    var a=Math.random()*Math.PI*2,d=30+Math.random()*70;
    s.style.setProperty('--tx',Math.cos(a)*d+'px');s.style.setProperty('--ty',Math.sin(a)*d+'px');
    s.style.setProperty('--d',(0.5+Math.random()*.8)+'s');
    s.style.left=e.clientX+'px';s.style.top=e.clientY+'px';
    document.body.appendChild(s);s.addEventListener('animationend',function(){{s.remove();}});}}
}});
</script>
</body>
</html>""".encode("utf-8")

class _DLHandler(BaseHTTPRequestHandler):
    filepath = ""; filename = ""; cfg = {}; page = b""
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            d = self.__class__.page
            self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8")
            self.send_header("Content-Length",str(len(d))); self.end_headers(); self.wfile.write(d)
        elif self.path.startswith("/download/"):
            try:
                with open(self.__class__.filepath,"rb") as f: d=f.read()
                self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8")
                self.send_header("Content-Disposition",f'attachment; filename="{self.__class__.filename}"')
                self.send_header("Content-Length",str(len(d))); self.end_headers(); self.wfile.write(d)
            except Exception as e: self.send_error(500,str(e))
        else: self.send_error(404)
    def log_message(self, *a): pass

class DownloadServer:
    PORT = 8080
    def __init__(self, filepath, cfg):
        cfg["_filepath"] = filepath
        fn = os.path.basename(filepath)
        _DLHandler.filepath = filepath; _DLHandler.filename = fn
        _DLHandler.cfg = cfg; _DLHandler.page = _dl_page(fn, cfg)
        self._srv = HTTPServer(("127.0.0.1", self.PORT), _DLHandler)
        self._t   = threading.Thread(target=self._srv.serve_forever, daemon=True)
    def start_and_open(self):
        self._t.start()
        url = f"http://localhost:{self.PORT}"
        print(f"\n  {GRN}✔ Download page → {YLW}{url}{R}")
        webbrowser.open(url)
    def stop(self):
        self._srv.shutdown()
        print(f"\n  {RED}⏹  Download server stopped.{R}")

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 7 — SPLASH & MENUS
# ══════════════════════════════════════════════════════════════════════════════

def splash():
    clr()
    rows = [
        "",
        f"{CYN}╔{'═'*62}╗{R}",
        f"{CYN}║{R}  {WHT}{BLD}██╗  ██╗ █████╗  ██████╗ ███████╗██████╗ ███████╗{R}         {CYN}║{R}",
        f"{CYN}║{R}  {WHT}{BLD}██║  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗██╔════╝{R}         {CYN}║{R}",
        f"{CYN}║{R}  {WHT}{BLD}███████║███████║██║  ███╗█████╗  ██████╔╝█████╗  {R}         {CYN}║{R}",
        f"{CYN}║{R}  {WHT}{BLD}██╔══██║██╔══██║██║   ██║██╔══╝  ██╔═══╝ ██╔══╝  {R}         {CYN}║{R}",
        f"{CYN}║{R}  {WHT}{BLD}██║  ██║██║  ██║╚██████╔╝███████╗██║     ███████╗{R}         {CYN}║{R}",
        f"{CYN}║{R}  {WHT}{BLD}╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚══════╝{R}         {CYN}║{R}",
        f"{CYN}╠{'═'*62}╣{R}",
        f"{CYN}║{R}  {MGT}{BLD}⚡  BEAST EDITION v4.0  —  Advanced Deface Generator  ⚡{R}  {CYN}║{R}",
        f"{CYN}║{R}  {YLW}Developer  : CyberKallan       GitHub  : CyberKallan{R}       {CYN}║{R}",
        f"{CYN}║{R}  {GRN}Recoded by : Hypervenom        Insta   : @imarjunarz{R}        {CYN}║{R}",
        f"{CYN}╚{'═'*62}╝{R}",
        "",
    ]
    for row in rows:
        print(row); time.sleep(0.03)

def main_menu():
    items = [
        ("1", "🛠   Create New Deface Page"),
        ("2", "💾  Load Saved Profile"),
        ("3", "👁   Preview Last Generated Page"),
        ("4", "📥  Download Page  (Local Server)"),
        ("5", "ℹ   About / Credits"),
        ("0", "🚪  Exit"),
    ]
    print(f"\n  {CYN}{BLD}┌─ MAIN MENU {'─'*46}┐{R}")
    for k, v in items:
        col = YLW if k != "0" else RED
        print(f"  {CYN}│{R}  {col}{BLD}{k}{R}  {WHT}{v}{R}")
    print(f"  {CYN}{BLD}└{'─'*58}┘{R}")
    return input(f"\n  {GRN}❯ Choose: {R}").strip()

# ── Theme ASCII preview grid ───────────────────────────────────────────────────
def print_theme_grid():
    print()
    items = list(THEMES.items())
    for row_items in [items[:5], items[5:]]:
        top = mid = bot = "  "
        for k, (name, acc, _) in row_items:
            c = THEME_TERM_COLORS.get(k, WHT)
            top += f"{c}┌──────────┐{R}  "
            mid += f"{c}│{R}{BLD}{k:>2}{R}{c}.{name:<7}{c}│{R}  "
            bot += f"{c}└──────────┘{R}  "
        print(top); print(mid); print(bot); print()

# ── Build wizard ──────────────────────────────────────────────────────────────
def wizard(last_cfg=None):
    clr(); splash()
    d = last_cfg or CONFIG_DEFAULTS

    print(f"\n  {CYN}{BLD}╔─ PAGE DETAILS {'─'*44}╗{R}")
    print(f"  {DIM}  Press Enter to keep the value shown in [ ]{R}\n")

    cfg = {}
    cfg["title"]         = ask("Page Title",                     d.get("title","Hacked"))
    cfg["heading"]       = ask("Main Heading",                   d.get("heading","YOU HAVE BEEN PWNED"))
    cfg["subheading"]    = ask("Sub-Heading  (optional)",        d.get("subheading",""))
    cfg["imagelink"]     = ask("Logo / Image URL",               d.get("imagelink",""))
    cfg["bgimage"]       = ask("Background Image URL",           d.get("bgimage",""))
    cfg["message"]       = ask("Message  (use <br> for newlines)", d.get("message","System compromised."))
    cfg["textcolor"]     = ask("Text Color  (hex or name)",      d.get("textcolor","#ffffff"))
    cfg["contact_email"] = ask("Contact Email  (optional)",      d.get("contact_email",""))

    # Media
    print(f"\n  {MGT}{BLD}┌─ AUDIO / VIDEO {'─'*42}┐{R}")
    print(f"  {DIM}  Supports: YouTube links, direct .mp3 URLs, SoundCloud URLs{R}")
    raw = ask("Paste URL  (or leave blank)", d.get("raw_media",""))
    cfg["raw_media"] = raw
    if raw:
        print(f"  {DIM}  Detecting media type...{R}", end=" ", flush=True)
        mtype, embed = resolve_media(raw)
        cfg["media_type"]  = mtype
        cfg["media_embed"] = embed
        labels = {"youtube": f"{GRN}▶ YouTube iframe (auto-converted){R}",
                  "mp3":     f"{GRN}🔊 Direct MP3 audio{R}",
                  "soundcloud": f"{GRN}☁ SoundCloud player{R}",
                  "unknown": f"{YLW}⚠ Unknown — will try as audio{R}"}
        print(f"  {labels.get(mtype, mtype)}")
    else:
        cfg["media_type"] = "none"; cfg["media_embed"] = ""

    # Theme
    print(f"\n  {CYN}{BLD}┌─ THEME {'─'*50}┐{R}")
    print_theme_grid()
    cfg["theme"] = ask_choice("Theme Number (1-10)", [str(i) for i in range(1,11)], d.get("theme","1"))

    # Font
    print(f"\n  {MGT}{BLD}┌─ FONT {'─'*51}┐{R}")
    for k,v in FONTS.items():
        print(f"    {YLW}{k}{R}. {WHT}{v}{R}")
    cfg["font"] = ask_choice("Font Number (1-6)", list(FONTS.keys()), d.get("font","1"))

    # Mobile
    print(f"\n  {BLU}{BLD}┌─ MOBILE MODE {'─'*44}┐{R}")
    cfg["mobile"] = ask_yn("Enable Mobile-First Responsive Mode?", d.get("mobile", False))

    # Encryption
    print(f"\n  {RED}{BLD}┌─ ENCRYPTION {'─'*45}┐{R}")
    cfg["encrypt"] = ask_yn("Password-protect this page?", d.get("encrypt", False))
    cfg["password"] = ask("Set Password", d.get("password","hackme")) if cfg["encrypt"] else ""

    # Output filename
    default_fn = cfg["title"].lower().replace(" ","_") + ".html"
    cfg["filename"] = ask("\nOutput filename", d.get("filename", default_fn))
    if not cfg["filename"].endswith(".html"):
        cfg["filename"] += ".html"

    return cfg

# ── Generate ──────────────────────────────────────────────────────────────────
def generate(cfg):
    clr(); splash()
    steps = [
        ("Parsing configuration",                           CYN),
        ("Resolving theme & palette",                       MGT),
        ("Building HTML structure",                         BLU),
        ("Injecting animations & canvas effects",           YLW),
        ("Applying mobile optimizations" if cfg.get("mobile") else "Skipping mobile layer", GRN),
        ("Encrypting page" if cfg.get("encrypt") else "Skipping encryption layer",          RED),
        ("Writing output file",                             GRN),
    ]
    print(f"\n  {CYN}{BLD}┌─ GENERATING {'─'*44}┐{R}\n")
    for label, col in steps:
        progress(label, col)

    html = build_html(cfg)
    if cfg.get("encrypt") and cfg.get("password"):
        html = apply_encryption(html, cfg["password"])

    out_dir  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, cfg["filename"])
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    # Auto-save profile
    prof_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles")
    os.makedirs(prof_dir, exist_ok=True)
    with open(os.path.join(prof_dir, "last.json"), "w") as f:
        json.dump(cfg, f, indent=2)

    _success_screen(cfg, out_path)
    return out_path

def _success_screen(cfg, out_path):
    tname = THEMES[cfg["theme"]][0]
    fname = FONTS.get(cfg["font"], "?")
    enc   = f"{RED}🔐 ENCRYPTED{R}" if cfg.get("encrypt") else f"{GRN}🔓 Open{R}"
    mob   = f"{BLU}📱 Mobile-First{R}" if cfg.get("mobile") else f"{DIM}Standard{R}"
    media = {"youtube":"▶ YouTube","mp3":"🔊 MP3","soundcloud":"☁ SoundCloud","none":"—"}.get(cfg.get("media_type","none"),"—")
    print(f"""
  {GRN}{BLD}╔══════════════════════════════════════════════════════════╗
  ║   ✅  PAGE GENERATED SUCCESSFULLY!                      ║
  ╠══════════════════════════════════════════════════════════╣{R}
  {WHT}  📄 File      : {YLW}{cfg['filename']}{R}
  {WHT}  📁 Saved to  : {DIM}{out_path}{R}
  {WHT}  🎨 Theme     : {CYN}{tname}{R}
  {WHT}  🔤 Font      : {MGT}{fname}{R}
  {WHT}  🎵 Media     : {YLW}{media}{R}
  {WHT}  🔒 Encrypt   : {enc}
  {WHT}  📱 Mobile    : {mob}
  {GRN}{BLD}╠══════════════════════════════════════════════════════════╣
  ║                                                          ║
  ║   Developer  : CyberKallan  │  GitHub  : CyberKallan    ║
  ║   Recoded by : Hypervenom   │  Insta   : @imarjunarz    ║
  ║                                                          ║
  ╚══════════════════════════════════════════════════════════╝{R}
""")

# ── Credits ───────────────────────────────────────────────────────────────────
def show_credits():
    clr(); splash()
    print(f"""
  {CYN}{BLD}╔══════════════════════════════════════════════════════════╗
  ║                    ABOUT THIS TOOL                       ║
  ╠══════════════════════════════════════════════════════════╣{R}
  {WHT}  Tool       {CYN}HagePe Deface Generator  v4.0 BEAST EDITION{R}
  {WHT}  Developer  {YLW}CyberKallan{R}  {DIM}— GitHub: CyberKallan{R}
  {WHT}  Recoded by {BLD}{WHT}Hypervenom{R}  {DIM}— Instagram: @imarjunarz{R}

  {CYN}{BLD}╠══════════════════════════════════════════════════════════╣{R}
  {GRN}  ✔{R}  YouTube / MP3 / SoundCloud auto-embed fixer
  {GRN}  ✔{R}  Live Preview Server  (localhost:7070)
  {GRN}  ✔{R}  Animated Download Page Server  (localhost:8080)
  {GRN}  ✔{R}  Mobile-First Responsive Mode
  {GRN}  ✔{R}  AES-style page encryption with SHA-256 password gate
  {GRN}  ✔{R}  10 Themes × 6 Fonts × full animation engine
  {GRN}  ✔{R}  Matrix rain + connected particle field canvas effects
  {GRN}  ✔{R}  Click spark effects, typewriter heading animation
  {GRN}  ✔{R}  Profile auto-save / reload
  {CYN}{BLD}╚══════════════════════════════════════════════════════════╝{R}
""")
    input(f"  {DIM}Press Enter to go back...{R}")

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 8 — MAIN LOOP
# ══════════════════════════════════════════════════════════════════════════════

def main():
    last_file = None
    last_cfg  = None

    splash()
    progress("Loading core modules",   CYN)
    progress("Initialising servers",   MGT)
    progress("Ready",                  GRN)
    time.sleep(0.2)

    while True:
        clr(); splash()
        choice = main_menu()

        if choice == "1":
            cfg       = wizard(last_cfg)
            last_file = generate(cfg)
            last_cfg  = cfg
            input(f"\n  {DIM}Press Enter to return to menu...{R}")

        elif choice == "2":
            p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles", "last.json")
            if os.path.exists(p):
                with open(p) as f: last_cfg = json.load(f)
                print(f"\n  {GRN}✔ Profile loaded: {last_cfg.get('filename','?')}{R}")
            else:
                print(f"\n  {YLW}⚠  No saved profile found. Create a page first.{R}")
            time.sleep(1.5)

        elif choice == "3":
            if last_file and os.path.exists(last_file):
                srv = PreviewServer(last_file)
                srv.start_and_open()
                input(f"\n  {DIM}Preview running at localhost:7070 — Press Enter to stop...{R}")
                srv.stop()
            else:
                print(f"\n  {YLW}⚠  No page generated yet. Use option 1 first.{R}")
                time.sleep(1.5)

        elif choice == "4":
            if last_file and os.path.exists(last_file):
                srv = DownloadServer(last_file, last_cfg or {})
                srv.start_and_open()
                input(f"\n  {DIM}Download page at localhost:8080 — Press Enter to stop...{R}")
                srv.stop()
            else:
                print(f"\n  {YLW}⚠  No page generated yet. Use option 1 first.{R}")
                time.sleep(1.5)

        elif choice == "5":
            show_credits()

        elif choice == "0":
            clr()
            print(f"\n  {CYN}Developer: CyberKallan  │  Recoded by: Hypervenom{R}")
            print(f"  {DIM}Goodbye.{R}\n")
            sys.exit(0)

if __name__ == "__main__":
    main()
