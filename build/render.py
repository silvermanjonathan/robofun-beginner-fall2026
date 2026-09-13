import html
import json
import os
import re
import tempfile
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from standards import STANDARDS, RESOLVED_ON, CONNECTOR
from sessions_a import SESSIONS_A
from sessions_b import SESSIONS_B
from sessions_c import SESSIONS_C

SESSIONS = SESSIONS_A + SESSIONS_B + SESSIONS_C
# Paths are relative to this file, so the repo runs from wherever it is cloned.
# The pages live in the repo root, one level up from build/.
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.environ.get("BVC_OUT", ROOT)
VERSION = "6"
REPO = "robofun-beginner-fall2026"
PUBLISHED = "2026-09-12"
TMP = os.environ.get("BVC_TMP",
                     os.path.join(tempfile.gettempdir(), "bvc_beginner_build"))

os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

# ---------------------------------------------------------------- verification

HEADLESS_PREAMBLE = '''
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
import pygame
_MAXF = {maxf}
_INJ = {inj}
_state = {{"f": 0}}

def _get(*a, **k):
    _state["f"] = _state["f"] + 1
    f = _state["f"]
    if f > _MAXF:
        return [pygame.event.Event(pygame.QUIT)]
    evs = []
    for item in _INJ:
        if item[0] == f and item[1] == "KEYDOWN":
            evs.append(pygame.event.Event(pygame.KEYDOWN, {{"key": getattr(pygame, item[2])}}))
    return evs

pygame.event.get = _get

class _Keys:
    def __init__(self, held):
        self.held = held
    def __getitem__(self, k):
        return k in self.held

def _gp(*a, **k):
    f = _state["f"]
    held = set()
    for item in _INJ:
        if item[0] == f and item[1] in ("KEYDOWN", "HOLD"):
            held.add(getattr(pygame, item[2]))
    return _Keys(held)

pygame.key.get_pressed = _gp
'''

VERIFY_LOG = []


ECHO_INPUT = '''
# Installed by build/render.py so captured output shows the typed answer after
# the prompt, the way a student's terminal does. Piped stdin does not echo.
import builtins
import sys as _sys
_real_input = builtins.input
def _echo_input(prompt=""):
    line = _sys.stdin.readline()
    if line == "":
        raise EOFError("EOF when reading a line")
    answer = line.rstrip("\\n")
    print(str(prompt) + answer)
    return answer
builtins.input = _echo_input
'''


def run_snippet(code, stdin=None, timeout=30, preamble="", fname="snippet.py"):
    path = os.path.join(TMP, fname)
    with open(path, "w") as fh:
        fh.write(preamble + code + "\n")
    env = dict(os.environ)
    if stdin is not None:
        with open(os.path.join(TMP, "sitecustomize.py"), "w") as fh:
            fh.write(ECHO_INPUT)
        env["PYTHONPATH"] = TMP + os.pathsep + env.get("PYTHONPATH", "")
    try:
        proc = subprocess.run(
            [sys.executable, path],
            input=(stdin or ""),
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return "TIMEOUT", 1
    out = proc.stdout
    err = proc.stderr.replace(TMP + "/", "").replace(TMP, "")
    if err.strip():
        lines = [ln for ln in err.rstrip().splitlines()
                 if "pygame community" not in ln
                 and not ln.startswith("pygame ")
                 and not ln.startswith("Hello from")]
        trimmed = "\n".join(ln.rstrip() for ln in lines if ln.strip())
        if out.strip():
            return out.rstrip() + "\n" + trimmed, proc.returncode
        return trimmed, proc.returncode
    clean = [ln for ln in out.splitlines() if "pygame community" not in ln]
    clean = [ln for ln in clean if not ln.startswith("pygame 2.")]
    return "\n".join(clean).rstrip(), proc.returncode


def verify(chunk, tag):
    mode = chunk.get("run")
    if mode is None:
        return None, None
    num = tag.split("-")[0].replace("s", "")
    if num == "13":
        fname = "Jonathan_friday_bonus.py"
    else:
        fname = "Jonathan_session%02d.py" % int(num)
    if mode == "compile":
        path = os.path.join(TMP, "compile_check.py")
        with open(path, "w") as fh:
            fh.write(chunk["code"] + "\n")
        proc = subprocess.run(
            [sys.executable, "-c",
             "import ast,sys; ast.parse(open(sys.argv[1]).read())", path],
            capture_output=True, text=True)
        ok = proc.returncode == 0
        VERIFY_LOG.append([tag, "compile", "ok" if ok else "FAIL"])
        if not ok:
            raise SystemExit("compile check failed for " + tag + "\n" + proc.stderr)
        return None, "compile"
    if mode == "headless":
        pre = HEADLESS_PREAMBLE.format(
            maxf=chunk.get("frames", 5),
            inj=json.dumps(chunk.get("inject", [])),
        )
        pre = pre + chunk.get("prefix", "")
        out, rc = run_snippet(chunk["code"], preamble=pre, timeout=90, fname=fname)
    else:
        out, rc = run_snippet(chunk["code"], preamble=chunk.get("prefix", ""),
                              stdin=chunk.get("stdin"), timeout=30, fname=fname)
    if out == "TIMEOUT":
        raise SystemExit("snippet timed out: " + tag)
    VERIFY_LOG.append([tag, mode, "rc=" + str(rc), str(len(out.splitlines())) + " lines"])
    return out, mode


# ---------------------------------------------------------------------- styling

CSS = """
/* Lecture Light: built for a projector in a room with the lights on.
   Light ground, near-black text, few accents, no hairlines. */
:root{
  --paper:#F4F0E6;
  --card:#FFFDF7;
  --ink:#17181B;
  --ink-soft:#4A4D53;
  --rule:#D3CBB8;
  --teal:#0E4D52;
  --teal-deep:#0A3A3E;
  --clay:#9C2B22;
  --ochre:#8A5A00;
  --ochre-line:#D99B12;
  --ochre-tint:#FBF2DC;
  --green:#1D5B39;
  --green-tint:#E8F1E9;
  --green-ink:#122B1C;
  --code-bg:#EDE7D9;
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:'DM Sans',system-ui,sans-serif; font-size:18px; font-weight:500;
  line-height:1.65;
}
header.top{
  background:var(--teal); color:#FFFDF7;
  border-bottom:6px solid var(--ochre-line); padding:30px 22px 26px;
}
.wrap{max-width:900px; margin:0 auto}
.eyebrow{
  font-family:'JetBrains Mono',monospace; font-size:13px; letter-spacing:.14em;
  text-transform:uppercase; color:#F2D89B; margin:0 0 10px; font-weight:700;
}
h1{
  font-family:'Bricolage Grotesque','DM Sans',sans-serif; font-weight:800;
  font-size:clamp(29px,4.8vw,44px); line-height:1.1; margin:0 0 10px;
}
h2{
  font-family:'Bricolage Grotesque','DM Sans',sans-serif; font-weight:700;
  font-size:25px; line-height:1.2; margin:0 0 12px; color:var(--teal-deep);
}
h3{
  font-family:'Bricolage Grotesque','DM Sans',sans-serif; font-weight:700;
  font-size:20px; margin:0 0 8px; color:var(--teal-deep);
}
header.top h1,header.top h2{color:#FFFDF7}
.sub{color:#EAE3D2; margin:0 0 16px; font-size:19px; font-weight:400}
.dates{
  display:flex; flex-wrap:wrap; gap:10px; margin-top:16px;
  font-family:'JetBrains Mono',monospace; font-size:13.5px;
}
.pill{
  border:2px solid rgba(255,253,247,.4); border-radius:999px; padding:5px 13px;
  background:rgba(255,253,247,.08);
}
.pill b{color:#F2D89B; font-weight:700}
main{padding:28px 22px 12px}
section{
  background:var(--card); border:2px solid var(--rule); border-radius:6px;
  padding:22px 24px; margin:0 0 20px;
}
section.opener{border-left:8px solid var(--green)}
section.chunk{border-left:8px solid var(--ochre-line)}
section.hinge{border-left:8px solid var(--clay)}
section.brief{border-left:8px solid var(--teal)}
.chunk-no{
  font-family:'JetBrains Mono',monospace; font-size:13px; letter-spacing:.12em;
  text-transform:uppercase; color:var(--ochre); margin:0 0 8px; font-weight:700;
}
p{margin:0 0 14px}
ul,ol{margin:0 0 14px; padding-left:24px}
li{margin:0 0 8px}
code{
  font-family:'JetBrains Mono',monospace; font-size:.9em; font-weight:700;
  background:var(--code-bg); color:#1E2A2B;
  padding:2px 6px; border-radius:3px;
}
pre{
  font-family:'JetBrains Mono',monospace; font-size:15.5px; line-height:1.6;
  background:var(--code-bg); color:var(--ink); border:2px solid var(--rule);
  border-left:6px solid #B9AF96; border-radius:4px;
  padding:16px 18px; overflow-x:auto; margin:0 0 16px; font-weight:500;
}
pre.out{
  background:var(--green-tint); border-color:#A9C6B2;
  border-left:6px solid var(--green); color:var(--green-ink);
}
.outlabel{
  font-family:'JetBrains Mono',monospace; font-size:12.5px; letter-spacing:.1em;
  text-transform:uppercase; color:var(--green); margin:0 0 7px; font-weight:700;
}
.predict{
  border:2px dashed var(--ochre); border-radius:5px;
  padding:16px 18px; margin:0 0 16px; background:var(--ochre-tint);
}
.predict p{margin:0 0 12px}
.predict .q{font-weight:700}
button.rev{
  font-family:'DM Sans',sans-serif; font-size:16px; font-weight:700;
  background:var(--teal); color:#FFFDF7; border:0; border-radius:4px;
  padding:10px 18px; cursor:pointer;
}
button.rev:hover{background:var(--teal-deep)}
.ans{display:none; margin-top:16px; padding-top:16px; border-top:2px solid var(--rule)}
.ans.open{display:block}
table{border-collapse:collapse; width:100%; margin:0 0 16px; font-size:16.5px}
th,td{border:2px solid var(--rule); padding:9px 11px; text-align:left; vertical-align:top}
th{background:#EFE9DA; font-weight:700; font-size:15px; color:var(--teal-deep)}
td.fill{background:#FBF9F3; min-width:100px}
.exits{display:grid; gap:14px; grid-template-columns:1fr}
@media(min-width:760px){.exits{grid-template-columns:repeat(3,1fr)}}
.exit{border:2px solid var(--rule); border-radius:5px; padding:16px}
.exit .tag{
  font-family:'JetBrains Mono',monospace; font-size:12.5px; letter-spacing:.1em;
  text-transform:uppercase; margin:0 0 8px; font-weight:700;
}
.exit.floor{border-top:6px solid var(--green)}
.exit.floor .tag{color:var(--green)}
.exit.middle{border-top:6px solid var(--ochre-line)}
.exit.middle .tag{color:var(--ochre)}
.exit.stretch{border-top:6px solid var(--clay)}
.exit.stretch .tag{color:var(--clay)}
details.teacher{
  background:var(--card); border:2px solid var(--rule);
  border-left:8px solid var(--clay); border-radius:6px;
  padding:18px 22px; margin:0 0 20px;
}
details.teacher summary{
  cursor:pointer; font-family:'Bricolage Grotesque','DM Sans',sans-serif;
  font-weight:700; font-size:21px; color:var(--clay);
}
details.teacher[open] summary{margin-bottom:14px}
.note{
  font-size:16.5px; color:var(--ink-soft); border-left:4px solid var(--rule);
  padding-left:14px; margin:0 0 14px;
}
.pager{
  max-width:900px; margin:0 auto; padding:8px 22px 34px;
  display:flex; justify-content:space-between; gap:12px;
  font-family:'JetBrains Mono',monospace; font-size:14px;
}
.pager a{
  color:var(--teal); text-decoration:none; font-weight:700;
  border:2px solid var(--rule); background:var(--card);
  border-radius:4px; padding:10px 14px;
}
.pager a:hover{background:#EFE9DA}
footer{
  background:#EAE4D5; border-top:4px solid var(--teal); padding:22px 22px 36px;
  font-size:15px; color:var(--ink-soft);
}
footer a{color:var(--teal); font-weight:700}
a{color:var(--teal)}
.grid2{display:grid; gap:16px; grid-template-columns:1fr}
@media(min-width:760px){.grid2{grid-template-columns:1fr 1fr}}
.card{border:2px solid var(--rule); border-radius:5px; padding:16px; background:#FFFDF7}
.card h3{margin-bottom:8px}
.sessionlist{list-style:none; padding:0; margin:0}
.sessionlist li{
  border:2px solid var(--rule); border-left:8px solid var(--teal);
  border-radius:5px; margin:0 0 12px; padding:14px 16px;
  display:flex; gap:16px; align-items:flex-start; background:#FFFDF7;
}
.sessionlist .n{
  font-family:'JetBrains Mono',monospace; font-size:24px; font-weight:700;
  color:var(--teal); min-width:38px;
}
.sessionlist a{font-weight:700; text-decoration:none; font-size:19px}
.sessionlist .meta{
  font-family:'JetBrains Mono',monospace; font-size:13px; color:var(--ink-soft);
  display:block; margin-top:4px;
}
.bonus{border-left-color:var(--clay)}
.bonus .n{color:var(--clay)}
.flag{
  background:#F7E4E1; border:2px solid var(--clay); border-left:8px solid var(--clay);
  border-radius:5px; padding:14px 16px; margin:0 0 18px; font-size:16.5px;
  color:#3A1512;
}
.stamp{
  border:3px dashed #BFB49A; border-radius:5px; padding:14px;
  font-size:15px; min-height:100px; background:#FFFDF7;
}
.stampgrid{display:grid; gap:12px; grid-template-columns:1fr 1fr}
@media(min-width:820px){.stampgrid{grid-template-columns:repeat(3,1fr)}}
.stamp .no{
  font-family:'JetBrains Mono',monospace; color:var(--ochre); font-size:12.5px;
  letter-spacing:.1em; text-transform:uppercase; display:block; margin-bottom:6px;
  font-weight:700;
}
@media print{
  body{background:#fff; font-size:11pt}
  header.top{background:#fff; color:#111; border-bottom:3px solid #111}
  header.top h1,header.top .sub,header.top .eyebrow,.pill b{color:#111}
  .pill{border-color:#666}
  footer,.pager,details.teacher{background:#fff}
  section,.stamp,.card{background:#fff; break-inside:avoid}
  .noprint{display:none}
  a{color:#111}
}
"""

JS = """
document.addEventListener('click', function(e){
  var b = e.target.closest('button.rev');
  if(!b) return;
  var t = document.getElementById(b.getAttribute('data-target'));
  if(!t) return;
  var open = t.classList.toggle('open');
  b.setAttribute('aria-expanded', open ? 'true' : 'false');
  b.textContent = open ? b.getAttribute('data-hide') : b.getAttribute('data-show');
});
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?'
         'family=Bricolage+Grotesque:opsz,wght@12..96,400..800&'
         'family=DM+Sans:wght@400;500;700&'
         'family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">')


def page(title, body, hub_label="Course home"):
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>' + html.escape(title) + '</title>\n'
        + FONTS + '\n<style>' + CSS + '</style>\n</head>\n<body>\n'
        + body +
        '\n<script>' + JS + '</script>\n</body>\n</html>\n'
    )


def link(slug):
    return slug + ".html?v=" + VERSION


def code_block(code):
    return '<pre>' + html.escape(code) + '</pre>'


def out_block(text, label="What actually happens"):
    return ('<p class="outlabel">' + label + '</p><pre class="out">'
            + html.escape(text) + '</pre>')


def reveal(idx, question, answer, qlabel="Predict", extra="",
           show="Show the answer", hide="Hide the answer"):
    return (
        '<div class="predict"><p class="q">' + qlabel + ': ' + question + '</p>'
        '<button class="rev" data-target="' + idx + '" aria-controls="' + idx + '" '
        'aria-expanded="false" data-show="' + show + '" '
        'data-hide="' + hide + '">' + show + '</button>'
        '<div class="ans" id="' + idx + '">' + extra + '<p>' + answer + '</p></div></div>'
    )


def standards_table(codes):
    rows = ""
    for c in codes:
        s = STANDARDS[c]
        rows += ('<tr><td><code>' + c + '</code></td><td>' + s["jurisdiction"]
                 + '</td><td>' + s["framework"] + '</td><td>' + s["grades"]
                 + '</td><td>' + html.escape(s["statement"]) + '</td></tr>')
    return ('<table><tr><th>Code</th><th>Jurisdiction</th><th>Framework</th>'
            '<th>Grade</th><th>Statement</th></tr>' + rows + '</table>')


# --------------------------------------------------------------- session pages

def render_session(s, prev_s, next_s):
    n = s["num"]
    bonus = s.get("bonus", False)
    label = "Bonus session" if bonus else "Session " + str(n) + " of 12"

    b = ['<header class="top"><div class="wrap">']
    b.append('<p class="eyebrow">Beyond Vibe Coding &middot; Beginner &middot; ' + label + '</p>')
    b.append('<h1>' + html.escape(s["title"]) + '</h1>')
    b.append('<p class="sub">' + html.escape(s["subtitle"]) + '</p>')
    b.append('<div class="dates">')
    b.append('<span class="pill"><b>Monday section</b> ' + s["mon"] + '</span>')
    b.append('<span class="pill"><b>Friday section</b> ' + s["fri"] + '</span>')
    b.append('<span class="pill"><b>Length</b> 90 minutes</span>')
    if s["new"]:
        b.append('<span class="pill"><b>New</b> ' + str(len(s["new"])) + ' items</span>')
    b.append('</div></div></header>')

    b.append('<main><div class="wrap">')

    if s["new"]:
        b.append('<section><h2>What is new today</h2><p>'
                 + ", ".join(html.escape(x) for x in s["new"]) + '.</p>')
    else:
        b.append('<section><h2>What is new today</h2><p>No new syntax. '
                 'Everything today uses what is already on your ledger card.</p>')
    if s["reuse"]:
        b.append('<p><b>Deliberately re-used:</b> ' + html.escape(s["reuse"]) + '.</p>')
    b.append('<p class="note">' + s["reuse_note"] + '</p></section>')

    op = s["opener"]
    b.append('<section class="opener"><p class="chunk-no">Opener &middot; '
             + str(op["minutes"]) + ' minutes</p><h2>' + html.escape(op["title"]) + '</h2>')
    b.append('<p>' + op["body"] + '</p>')
    for i, q in enumerate(op["questions"]):
        b.append(reveal("s%d-op%d" % (n, i), q["q"], q["a"], "Question"))
    b.append('</section>')

    for i, ch in enumerate(s["chunks"]):
        tag = "s%d-c%d" % (n, i + 1)
        out, mode = verify(ch, tag)
        b.append('<section class="chunk"><p class="chunk-no">Chunk ' + str(i + 1)
                 + ' of ' + str(len(s["chunks"])) + '</p>')
        b.append('<h2>' + html.escape(ch["title"]) + '</h2>')
        b.append('<p>' + ch["teach"] + '</p>')
        b.append(code_block(ch["code"]))
        if ch.get("prefix"):
            b.append('<p class="note">This sits in the same file as the program in chunk 3, '
                     'underneath it. Run the whole file.</p>')
        loops = "while running" in ch["code"]
        extra = ""
        if out:
            lbl = "What it actually prints"
            if mode == "headless" and loops:
                lbl = ("What it actually prints (run without a screen, quit after "
                       + str(ch.get("frames", 5)) + " frames)")
            elif mode == "headless":
                lbl = "What it actually prints (run without a screen)"
            extra = out_block(out, lbl)
        elif mode == "headless":
            tail = (" and quit after " + str(ch.get("frames", 5)) + " frames"
                    if loops else "")
            extra = ('<p class="note">Nothing printed in the terminal. This was run '
                     'without a screen' + tail + ', and it printed nothing because the '
                     'window is the output. Words go in the terminal, visuals go in the '
                     'window.</p>')
        b.append(reveal(tag, ch["predict"], ch["reveal"], "Predict", extra,
                        "Run it first, then check here", "Hide"))
        if mode == "compile":
            b.append('<p class="note">Checked for syntax here, but it needs a real '
                     'screen to draw on. Run it on a machine with a display.</p>')
        b.append('</section>')

    h = s["hinge"]
    m = re.match(r"From session (\d+)", h["q"])
    if m:
        cap = "reaches back to session " + m.group(1)
    elif h["q"].startswith("Pick any stamp"):
        cap = "reaches back across the ledger card"
    else:
        cap = "from today's chunks"
    b.append('<section class="hinge"><p class="chunk-no">Hinge question &middot; '
             + cap + '</p><h2>Before you build</h2>')
    b.append(reveal("s%d-hinge" % n, h["q"], h["a"], "Question"))
    b.append('</section>')

    br = s["brief"]
    b.append('<section class="brief"><p class="chunk-no">Build &middot; '
             + str(br["minutes"]) + ' minutes</p><h2>' + html.escape(br["title"]) + '</h2><ol>')
    for st in br["steps"]:
        b.append('<li>' + st + '</li>')
    b.append('</ol>')
    for j, card in enumerate(br.get("cards", [])):
        tag = "s%d-card%d" % (n, j + 1)
        out, mode = verify(card, tag)
        b.append('<h3>' + html.escape(card["title"]) + '</h3>')
        if card.get("teach"):
            b.append('<p>' + card["teach"] + '</p>')
        b.append(code_block(card["code"]))
        extra = ""
        if out:
            lbl = "What it actually prints"
            if mode == "headless":
                lbl = ("What it actually prints (run without a screen, quit after "
                       + str(card.get("frames", 5)) + " frames)")
            extra = out_block(out, lbl)
        b.append(reveal(tag, card["predict"], card["reveal"], "Predict", extra,
                        "Run it first, then check here", "Hide"))
    b.append('<h3>Expected and got</h3>'
             '<p>Fill in the left column before you run. Fill in the right column after.</p>')
    b.append('<table><tr><th>Expected</th><th>Got</th></tr>')
    for row in br["expected_got"]:
        b.append('<tr><td>' + row[0] + '</td><td class="fill"></td></tr>')
    b.append('</table></section>')

    ex = s["exits"]
    b.append('<section><h2>Where you can stop</h2>'
             '<p>All three are real landings. Nobody is behind for finishing at the floor.</p>'
             '<div class="exits">')
    b.append('<div class="exit floor"><p class="tag">Floor</p><p>' + ex["floor"] + '</p></div>')
    b.append('<div class="exit middle"><p class="tag">Middle</p><p>' + ex["middle"] + '</p></div>')
    b.append('<div class="exit stretch"><p class="tag">Stretch</p><p>' + ex["stretch"] + '</p></div>')
    b.append('</div></section>')

    b.append('<section><h2>Ledger card</h2><p>' + s["ledger"] + '</p>'
             '<p><a href="' + link("semester_ledger_card") + '">Open the semester ledger card</a></p></section>')

    t = s["teacher"]
    b.append('<details class="teacher"><summary>Teacher panel</summary>')
    b.append('<h3>Timing, 90 minutes</h3><ul>')
    for x in t["timing"]:
        b.append('<li>' + html.escape(x) + '</li>')
    b.append('</ul><p class="note">Honest pacing: most rooms will not reach the end of '
             'the build brief. The exits exist so that stopping is a landing rather than a failure.</p>')
    b.append('<h3>What you will see, and what to do</h3>'
             '<table><tr><th>In the room</th><th>Redirect</th></tr>')
    for m in t["misconceptions"]:
        b.append('<tr><td>' + m[0] + '</td><td>' + m[1] + '</td></tr>')
    b.append('</table>')
    b.append('<h3>Mapped to</h3>')
    b.append(standards_table(t["standards"]))
    lcs = []
    for c in t["standards"]:
        for l in STANDARDS[c]["lcs"]:
            lcs.append((c, l))
    if lcs:
        b.append('<h3>Learning components behind those codes</h3><ul>')
        for c, l in lcs:
            b.append('<li><code>' + c + '</code> ' + html.escape(l) + '</li>')
        b.append('</ul>')
    b.append('<h3>If time runs out</h3><p>' + t["routing"] + '</p>')
    b.append('</details>')

    if s.get("env_note"):
        b.append('<section><h2>Running this in VS Code</h2><div class="grid2">'
                 '<div class="card"><h3>Once, before the first run</h3>'
                 '<p>Open the terminal in VS Code and install the library: '
                 '<code>pip install pygame</code>. Check it worked with '
                 '<code>python -c "import pygame"</code>. It should print two lines of '
                 'greeting from pygame and nothing else. A traceback here is an install '
                 'problem, not a problem with your program. Those same two greeting lines '
                 'appear at the top of the terminal every time you run a pygame program; '
                 'the output boxes on this site leave them out.</p></div>'
                 '<div class="card"><h3>Every run after that</h3>'
                 '<p>The window often opens behind VS Code, so check the taskbar before '
                 'deciding nothing happened. Close it with its own close button: these '
                 'programs are written to end when the window closes, and stopping the '
                 'terminal instead can leave the window stuck on screen. A window that '
                 'will not close usually means the loop has no '
                 '<code>pygame.event.get()</code> in it.</p></div></div>'
                 '<p class="note">There is no turtle anywhere in this course. Turtle needs '
                 'a library our VS Code setup does not have, so pygame does all the drawing, '
                 'starting in session 5.</p></section>')

    b.append('</div></main>')

    b.append('<nav class="pager">')
    if prev_s:
        b.append('<a href="' + link(prev_s["slug"]) + '">&larr; '
                 + html.escape(prev_s["title"]) + '</a>')
    else:
        b.append('<span></span>')
    b.append('<a href="' + link("beginner_semester_hub") + '">Course home</a>')
    if next_s:
        b.append('<a href="' + link(next_s["slug"]) + '">'
                 + html.escape(next_s["title"]) + ' &rarr;</a>')
    else:
        b.append('<span></span>')
    b.append('</nav>')

    b.append('<footer><div class="wrap">'
             '<p>Beyond Vibe Coding, beginner semester, Robofun Fall 2026. '
             '110 West End Avenue. Monday and Friday sections run the same spine.</p>'
             '<p>Mapped to NY Next Generation Learning Standards and the Standards for '
             'Mathematical Practice. Codes resolved through the ' + CONNECTOR + ' on '
             + RESOLVED_ON + '. <a href="' + link("standards_map") + '">Full standards map</a> '
             '&middot; <a href="' + link("beginner_constraints") + '">Code constraints, '
             'published ' + PUBLISHED + '</a></p>'
             '</div></footer>')

    return page(s["title"] + " | Beyond Vibe Coding beginner", "".join(b))


# -------------------------------------------------------------------- hub page

def render_hub():
    b = ['<header class="top"><div class="wrap">']
    b.append('<p class="eyebrow">Robofun &middot; Fall 2026 &middot; 110 West End Avenue</p>')
    b.append('<h1>Beyond Vibe Coding: Python, beginner</h1>')
    b.append('<p class="sub">Twelve sessions of ninety minutes. You read the code, '
             'trace it out loud, and then run it. Monday and Friday are separate classes '
             'working through the same twelve sessions.</p>')
    b.append('<div class="dates">'
             '<span class="pill"><b>Monday</b> Sep 14 to Dec 14, 12 sessions</span>'
             '<span class="pill"><b>Friday</b> Sep 18 to Dec 18, 12 sessions plus 1 bonus</span>'
             '<span class="pill"><b>Grades</b> 5 to 8</span>'
             '<span class="pill"><b>Demo day</b> the last session of each section</span>'
             '</div></div></header>')

    b.append('<main><div class="wrap">')

    b.append('<section><h2>How a session runs</h2>'
             '<p>Every session has the same shape, because at least a week passes between '
             'classes, sometimes two, and the first ten minutes are for getting things '
             'back.</p>'
             '<ol>'
             '<li><b>Retrieval opener, 10 minutes.</b> Two questions on paper about work from '
             'one and two sessions ago. No editor until both are written down.</li>'
             '<li><b>Chunks, 45 to 65 minutes.</b> One idea each. You predict what the code '
             'will do before you run it, then you run it and read what actually happened.</li>'
             '<li><b>Hinge question.</b> One question that reaches back to an earlier session, or to today, answered '
             'before the build starts.</li>'
             '<li><b>Build, 10 to 25 minutes.</b> A brief with an expected and got sheet. The '
             'expected column gets filled in first.</li>'
             '<li><b>Exit and ledger stamp, 5 to 10 minutes.</b> Floor, middle, and stretch are '
             'all real landings. One stamp goes on the semester card.</li>'
             '</ol></section>')

    b.append('<section><h2>The twelve sessions</h2><ul class="sessionlist">')
    for s in SESSIONS:
        cls = ' class="bonus"' if s.get("bonus") else ''
        num = "B" if s.get("bonus") else str(s["num"])
        b.append('<li' + cls + '><span class="n">' + num + '</span><div>'
                 '<a href="' + link(s["slug"]) + '">' + html.escape(s["title"]) + '</a>'
                 '<span class="meta">' + s["mon"] + ' &middot; ' + s["fri"] + '</span>'
                 '<span class="meta">' + html.escape(s["subtitle"]) + '</span>'
                 '</div></li>')
    b.append('</ul></section>')

    b.append('<section><h2>Course pages</h2><div class="grid2">'
             '<div class="card"><h3><a href="' + link("beginner_constraints")
             + '">Code constraints</a></h3><p>What is in this course and what is left out, '
             'published ' + PUBLISHED + ' with one frame loop and one list of exclusions. '
             'Read this before writing any lesson material.</p></div>'
             '<div class="card"><h3><a href="' + link("semester_ledger_card")
             + '">Semester ledger card</a></h3><p>One printed page that grows by one stamp '
             'a week. It is the only thing that survives between sessions, so it carries the '
             'syntax students cannot look up at home.</p></div>'
             '<div class="card"><h3><a href="' + link("standards_map")
             + '">Standards map</a></h3><p>Every code used in the course, with its '
             'jurisdiction, framework, and full statement, resolved through the '
             + CONNECTOR + '.</p></div>'
             '<div class="card"><h3>Float topics</h3><p>Not built. Held for cancellations and '
             'for a section that runs ahead: file input and output for a high score that '
             'survives a restart, sine waves and circular motion, and coaster energy. A GUI '
             'float was dropped: tkinter is not available, and a pygame version would need '
             'on-screen labels, which <code>pygame.font</code> is excluded from '
             'providing.</p></div>'
             '</div></section>')

    b.append('<section><h2>Calendar, by section</h2>'
             '<div class="flag"><b>Verify before you commit.</b> The dates below assume '
             'Robofun is closed Mon Sep 21 for Yom Kippur, Mon Oct 12 for Columbus and '
             'Indigenous Peoples Day, and Fri Nov 27 for the day after Thanksgiving. '
             'Fri Oct 2 falls in the intermediate days of Sukkot, which some Upper West Side '
             'programs skip. Check the published closure list and adjust.</div>')
    b.append('<div class="grid2">')
    b.append('<div class="card"><h3>Monday, 12 sessions</h3><table>'
             '<tr><th>Date</th><th>Session</th></tr>')
    for s in SESSIONS:
        if s.get("bonus"):
            continue
        b.append('<tr><td>' + s["mon"] + '</td><td>' + str(s["num"]) + '. '
                 + html.escape(s["title"]) + '</td></tr>')
    b.append('</table></div>')
    b.append('<div class="card"><h3>Friday, 12 sessions plus a bonus</h3><table>'
             '<tr><th>Date</th><th>Session</th></tr>')
    fri = sorted(SESSIONS, key=lambda s: ("Dec" in s["fri"], s["fri"]))
    order = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 12]
    by_num = {s["num"]: s for s in SESSIONS}
    for num in order:
        s = by_num[num]
        tag = "Bonus. " if s.get("bonus") else str(s["num"]) + ". "
        b.append('<tr><td>' + s["fri"] + '</td><td>' + tag + html.escape(s["title"])
                 + '</td></tr>')
    b.append('</table></div></div>')
    b.append('<p class="note">Monday is the short section, so the spine is twelve sessions '
             'and Friday spends its extra date on a bonus that nothing later depends on. '
             'If a parent compares the two classes, the required content is identical.</p>'
             '<p class="note">From session 4 on, Friday runs one to two sessions ahead of '
             'Monday, so in most weeks the two sections are on different pages. Each page '
             'shows both dates in its header. If Fri Oct 2 is lost to Sukkot, drop the '
             'bonus, move sessions 3 to 11 one Friday later, and keep session 12 on '
             'Dec 18.</p>')
    b.append('</section>')

    b.append('<section><h2>Machines and libraries</h2>'
             '<p>VS Code on the desktop, throughout. One graphics library, pygame, from '
             'session 5 onward, installed with <code>pip install pygame</code>. There is no '
             'turtle session and no second graphics library, because turtle does not run in '
             'our VS Code setup.</p></section>')
    b.append('<section><h2>What students cannot do at home</h2>'
             '<p>Assume no working Python between sessions. Nothing in this course is '
             'assigned as homework and nothing depends on work done outside the room. '
             'What travels home is the ledger card, on paper.</p></section>')

    b.append('<section><h2>Standards, in short</h2>'
             '<p>Every session maps to at most three standards, and every code on this site '
             'was resolved through the ' + CONNECTOR + ' on ' + RESOLVED_ON
             + ' rather than written from memory. The mathematics codes come from the New York '
             'Next Generation Mathematics Learning Standards and the Standards for '
             'Mathematical Practice. The reading, writing, and speaking codes come from the '
             'New York Next Generation ELA Learning Standards.</p>'
             '<div class="flag"><b>Not claimed here:</b> computer science standards. '
             'The New York Computer Science and Digital Fluency standards and the CSTA '
             'standards are not in the connector, so no CS code appears anywhere on this '
             'site. Add them by hand when you have the codes in front of you, at no more '
             'than three per session, footered as mapped to.</div>'
             '<p><a href="' + link("standards_map") + '">Open the full standards map</a></p>'
             '</section>')

    b.append('</div></main>')
    b.append('<footer><div class="wrap"><p>Beyond Vibe Coding, beginner semester, Robofun '
             'Fall 2026. Built ' + PUBLISHED + '. Version pin <code>?v=' + VERSION
             + '</code> on every internal link.</p></div></footer>')

    return page("Beyond Vibe Coding: Python, beginner | Robofun Fall 2026", "".join(b))


# ------------------------------------------------------------- constraints page

def render_constraints():
    b = ['<header class="top"><div class="wrap">']
    b.append('<p class="eyebrow">Beginner course &middot; published ' + PUBLISHED + '</p>')
    b.append('<h1>Code constraints</h1>')
    b.append('<p class="sub">What this course uses, what it leaves out, and the one frame '
             'loop. Every page on this site obeys this list. Changing the list means '
             'republishing it with a new date.</p></div></header>')
    b.append('<main><div class="wrap">')

    b.append('<section><h2>Allowed, and where each is first taught</h2>'
             '<p>Each of these is taught in a named session and not used before it.</p>'
             '<table>'
             '<tr><th>Now allowed</th><th>First taught</th><th>Why</th></tr>'
             '<tr><td><code>return</code></td><td>Session 4</td><td>Without it a function '
             'cannot be composed, tested, or reused, and every function hands back '
             '<code>None</code>.</td></tr>'
             '<tr><td><code>and</code>, <code>or</code></td><td>Session 2</td><td>With '
             'nesting banned there was no way to write two conditions at once.</td></tr>'
             '<tr><td><code>len</code>, <code>sum</code>, <code>max</code>, <code>min</code></td>'
             '<td>Session 3</td><td>Taught as the reveal after the hand-written version, '
             'never before it.</td></tr>'
             '<tr><td>String methods and slicing</td><td>Session 6</td><td>Students could '
             'not clean their own input, which forced capitals-and-spaces workarounds.</td></tr>'
             '<tr><td>Dictionaries</td><td>Session 9</td><td>The parallel-list failure is '
             'taught first, then the fix.</td></tr>'
             '<tr><td><code>.find()</code></td><td>Session 8</td><td>Revealed after the '
             'hand-written rack scan.</td></tr>'
             '<tr><td>pygame from session 5 onward</td><td>Session 5</td><td>The only graphics library in the course. It replaces the turtle drawing session, which does not run in VS Code.</td></tr>'
             '<tr><td>KEYDOWN, mouse, frame timers</td><td>Session 11</td><td>Without them a '
             'game reads as a demo. A held key and a single press are different '
             'questions.</td></tr>'
             '<tr><td><code>random.seed</code>, <code>randint</code></td><td>Session 3</td>'
             '<td>A seed is how you test a program that is supposed to be '
             'unpredictable.</td></tr>'
             '</table></section>')

    b.append('<section><h2>Still excluded, all twelve sessions</h2>'
             '<ul>'
             '<li><b>Nested gates.</b> Flat <code>if</code>, <code>elif</code>, '
             '<code>else</code> only. If a student reaches for an if inside an if, hand them '
             '<code>and</code>.</li>'
             '<li><b><code>break</code> and <code>continue</code>.</b> Every '
             '<code>while</code> names its exit condition in the condition itself.</li>'
             '<li><b><code>while True</code>.</b> Same reason.</li>'
             '<li><b><code>try</code> and <code>except</code>.</b> Ask-until-valid loops '
             'cover the same ground at this level.</li>'
             '<li><b><code>//</code>.</b> A single slash and <code>%</code> are enough.</li>'
             '<li><b><code>class</code>.</b> Advanced course material.</li>'
             '<li><b>Recursion, list comprehensions, lambda, <code>global</code>.</b></li>'
             '<li><b>Multi-file programs and importing your own module.</b> Advanced '
             'course.</li>'
             '<li><b>File input and output.</b> Held as a float, not in the spine.</li>'
             '<li><b><code>pygame.font</code>.</b> Words go in the terminal and visuals go '
             'in the window. That split holds all term.</li>'
             '<li><b>turtle.</b> Not used anywhere in this course. It needs a library our '
             'VS Code setup does not have, so pygame does all of the drawing, starting in '
             'session 5. No turtle program appears in this repo.</li>'
             '</ul></section>')

    b.append('<section><h2>The frame loop, and only this one</h2>'
             '<p>This course uses one frame loop, everywhere, with no exceptions. Students '
             'first copy it in session 5 as a harness holding '
             'a finished drawing on screen, and session 10 takes it apart.</p>')
    b.append(code_block('running = 1\nwhile running:\n    for event in pygame.event.get():\n'
                        '        if event.type == pygame.QUIT:\n            running = 0\n'
                        '    screen.fill(BG)\n    # draw here\n    pygame.display.flip()\n'
                        '    clock.tick(60)\npygame.quit()'))
    b.append('<p>A window never closes itself. It closes when the person closes it. Any '
             'program handed out in this course has this shape.</p>'
             '<p>Two placements of the drawing, both legitimate, and students meet them in '
             'this order. In session 5 the drawing is done once onto a '
             '<code>pygame.Surface</code> above the loop, and the loop only blits it, '
             'because the picture never changes. From session 10 on, the '
             '<code>fill</code> and the drawing sit inside the loop, because the picture '
             'changes every frame.</p></section>')

    b.append('<section><h2>Standing rules</h2><ul>'
             '<li><b>One change per run.</b> Change one thing, run it, write down what '
             'happened.</li>'
             '<li><b>Predict before you run.</b> Out loud or on paper, every chunk.</li>'
             '<li><b>Expected and got.</b> The expected column is filled in before the run, '
             'not after.</li>'
             '<li><b>Honest names.</b> A function called <code>check</code> that removes a '
             'life gets renamed. This is an exit criterion, not a style preference.</li>'
             '<li><b>Words in the terminal, visuals in the window.</b></li>'
             '<li><b>Knob block at the top.</b> Every number the behaviour depends on gets a '
             'capitalised name above the code that uses it.</li>'
             '</ul></section>')

    b.append('<section><h2>Verification</h2>'
             '<p>Every output box on every session page was produced by running that exact '
             'snippet, not typed from expectation. Terminal snippets were run with real '
             'input where they ask for it. The pygame snippets were run without a screen, '
             'with a quit event injected after a set number of frames, and the printed probe '
             'lines on those pages are the real ones. Every snippet on this site was run. '
             'Where a snippet continues a program from an earlier chunk, the page says so '
             'and the whole file was run together.</p></section>')

    b.append('</div></main>')
    b.append('<nav class="pager"><a href="' + link("beginner_semester_hub")
             + '">Course home</a><a href="' + link("standards_map")
             + '">Standards map &rarr;</a></nav>')
    b.append('<footer><div class="wrap"><p>Published ' + PUBLISHED
             + '.</p></div></footer>')
    return page("Code constraints | Beyond Vibe Coding beginner", "".join(b))


# ------------------------------------------------------------ standards mapping

def render_standards():
    used = {}
    for s in SESSIONS:
        for c in s["teacher"]["standards"]:
            used.setdefault(c, []).append(s)

    b = ['<header class="top"><div class="wrap">']
    b.append('<p class="eyebrow">Resolved ' + RESOLVED_ON + ' through the ' + CONNECTOR + '</p>')
    b.append('<h1>Standards map</h1>')
    b.append('<p class="sub">Every code used in this course, its full official statement, '
             'and the sessions it is mapped to. No code here was written from memory. Each '
             'one was returned by a lookup against the CASE Network, and the identifier is '
             'printed so it can be checked.</p></div></header>')
    b.append('<main><div class="wrap">')

    b.append('<section><h2>By session</h2>'
             '<p>At most three per session, footered as mapped to rather than aligned '
             'with.</p><table><tr><th>Session</th><th>Mapped to</th></tr>')
    for s in SESSIONS:
        name = ("Bonus" if s.get("bonus") else str(s["num"])) + '. ' + html.escape(s["title"])
        codes = " ".join('<code>' + c + '</code>' for c in s["teacher"]["standards"])
        b.append('<tr><td><a href="' + link(s["slug"]) + '">' + name + '</a></td><td>'
                 + codes + '</td></tr>')
    b.append('</table></section>')

    groups = [
        ("New York Next Generation Mathematics Learning Standards",
         [c for c in used if STANDARDS[c]["jurisdiction"] == "New York"
          and STANDARDS[c]["subject"] == "Mathematics"]),
        ("Standards for Mathematical Practice, Multi-State",
         [c for c in used if STANDARDS[c]["jurisdiction"] == "Multi-State"]),
        ("New York Next Generation ELA Learning Standards",
         [c for c in used if STANDARDS[c]["subject"] == "English Language Arts"]),
    ]
    for title, codes in groups:
        b.append('<section><h2>' + title + '</h2>')
        for c in sorted(codes):
            s = STANDARDS[c]
            sess = ", ".join(("Bonus" if x.get("bonus") else str(x["num"]))
                             for x in used[c])
            b.append('<div class="card" style="margin-bottom:12px"><h3><code>' + c
                     + '</code> &middot; grade ' + s["grades"] + '</h3>')
            b.append('<p>' + html.escape(s["statement"]) + '</p>')
            if s["lcs"]:
                b.append('<p><b>Learning components:</b></p><ul>')
                for l in s["lcs"]:
                    b.append('<li>' + html.escape(l) + '</li>')
                b.append('</ul>')
            b.append('<p class="note">Used in session ' + sess
                     + '. CASE identifier <code>' + s["uuid"] + '</code>.</p></div>')
        b.append('</section>')

    b.append('<section><h2>What is deliberately absent</h2>'
             '<p>No computer science standard appears on this site. The connector resolves '
             'New York mathematics and ELA codes and the Multi-State practice standards. It '
             'returned nothing for the New York Computer Science and Digital Fluency codes '
             'or for CSTA codes, and this course does not print codes it cannot verify. '
             'When the CS codes are in front of you, add at most three per session and keep '
             'the mapped to wording.</p>'
             '<p>The learning components listed above come from the same connector, for the '
             'standards that have them. They are the finer-grain skills behind a broad code '
             'and are useful for writing a single practice question that targets one '
             'thing.</p></section>')

    b.append('</div></main>')
    b.append('<nav class="pager"><a href="' + link("beginner_constraints")
             + '">&larr; Code constraints</a><a href="' + link("beginner_semester_hub")
             + '">Course home</a></nav>')
    b.append('<footer><div class="wrap"><p>Resolved ' + RESOLVED_ON + '. Re-resolve before '
             'distributing to families, since frameworks are revised.</p></div></footer>')
    return page("Standards map | Beyond Vibe Coding beginner", "".join(b))


# ------------------------------------------------------------------ ledger card

def render_ledger():
    b = ['<header class="top"><div class="wrap">']
    b.append('<p class="eyebrow">One page &middot; print it &middot; it grows weekly</p>')
    b.append('<h1>Semester ledger card</h1>')
    b.append('<p class="sub">Nothing about this course survives at home except this card. '
             'One stamp a week, written by hand, in the student\'s own words. Print it on '
             'card stock at the start of term and keep the stack in the room.</p>'
             '</div></header>')
    b.append('<main><div class="wrap">')
    b.append('<section class="noprint"><h2>How to use it</h2><ul>'
             '<li>Ten minutes at the end of each session. The student writes, not the '
             'teacher.</li>'
             '<li>One stamp per session, in the box for that session number.</li>'
             '<li>At least one error message per term, copied out by hand.</li>'
             '<li>The card comes out again in the retrieval opener the following week.</li>'
             '<li>Session 12 reads the card out loud. If a stamp is unreadable, that is the '
             'first thing fixed that day.</li></ul></section>')
    b.append('<section><h2>Stamps</h2><div class="stampgrid">')
    for s in SESSIONS:
        if s.get("bonus"):
            continue
        b.append('<div class="stamp"><span class="no">Stamp ' + str(s["num"]) + ' &middot; '
                 + html.escape(s["title"]) + '</span></div>')
    b.append('<div class="stamp"><span class="no">Bonus &middot; distance and bumpers</span>'
             '</div>')
    b.append('</div></section>')

    b.append('<section><h2>Reference strip</h2>'
             '<p>The syntax that is hardest to remember after a week away. Everything else '
             'goes in a stamp, in the student\'s handwriting.</p>')
    b.append(code_block(
        'name = value            store a value under a name\n'
        'int(text)               text to number, on its own line\n'
        'f"{name} has {n}"       drop values into a sentence\n'
        'if / elif / else        flat gates, never nested\n'
        '==  !=  <  >  <=  >=    comparisons, hand back True or False\n'
        'and / or                two conditions at once\n'
        'while condition:        names its own exit\n'
        'for i in range(5):      0 1 2 3 4, stops before 5\n'
        'list[0]                 first slot; last is len - 1\n'
        'text[0:3]               slots 0 1 2, stops before 3\n'
        'def f(x):               ...    return x * 2\n'
        'no return               hands back None\n'
        'd = {"key": value}      look up with d["key"]\n'
        'key in d                True or False, checks keys\n'
        'a % b                   remainder; wraps a counter\n'
        'rack.find(ch)           a slot, or -1 for not found\n'
        '360 / sides             the turn that closes a shape\n'
        'math.radians(deg)       convert before cos and sin\n'
        'cos is across, sin down the far end of a step\n'
        'draw.line(c, col, a, b, 3)  canvas, colour, start, end, width\n'
        'while running:          pygame frame loop, QUIT sets running = 0\n'
        'x = x + vx              move once per frame\n'
        'v = -v                  bounce\n'
        'level[row][col]         row first, then column'))
    b.append('<p class="note">Read the last line of an error first. One change per run.</p>')
    b.append('</section>')

    b.append('<section><h2>Error names met this term</h2>'
             '<p>Write the real message next to each one, the first time you meet it.</p>'
             '<table><tr><th>Name</th><th>What it usually means</th><th>Your message</th></tr>'
             '<tr><td>NameError</td><td>A word Python does not know. Often a typo.</td>'
             '<td class="fill"></td></tr>'
             '<tr><td>SyntaxError</td><td>Punctuation. A bracket, a colon, one equals sign '
             'where two belong.</td><td class="fill"></td></tr>'
             '<tr><td>IndentationError</td><td>A block is missing, or indented '
             'unevenly.</td><td class="fill"></td></tr>'
             '<tr><td>TypeError</td><td>Two kinds that will not mix. Usually text and '
             'number.</td><td class="fill"></td></tr>'
             '<tr><td>IndexError</td><td>A slot past the end. Length and last index are one '
             'apart.</td><td class="fill"></td></tr>'
             '<tr><td>KeyError</td><td>A dictionary key that is not there. Gate with '
             '<code>in</code>.</td><td class="fill"></td></tr>'
             '<tr><td>No error, wrong answer</td><td>A silent bug. Use a probe.</td>'
             '<td class="fill"></td></tr>'
             '</table></section>')

    b.append('</div></main>')
    b.append('<nav class="pager noprint"><a href="' + link("beginner_semester_hub")
             + '">Course home</a><a href="' + link("session01_printing_names_input")
             + '">Session 1 &rarr;</a></nav>')
    b.append('<footer><div class="wrap"><p>Beyond Vibe Coding beginner semester, Robofun '
             'Fall 2026.</p></div></footer>')
    return page("Semester ledger card | Beyond Vibe Coding beginner", "".join(b))


# ------------------------------------------------------------------------ write

def main():
    files = {}
    for i, s in enumerate(SESSIONS):
        prev_s = SESSIONS[i - 1] if i > 0 else None
        next_s = SESSIONS[i + 1] if i < len(SESSIONS) - 1 else None
        files[s["slug"] + ".html"] = render_session(s, prev_s, next_s)
        print("rendered", s["slug"])
    files["beginner_semester_hub.html"] = render_hub()
    files["beginner_constraints.html"] = render_constraints()
    files["standards_map.html"] = render_standards()
    files["semester_ledger_card.html"] = render_ledger()

    for name, text in files.items():
        with open(os.path.join(OUT, name), "w") as fh:
            fh.write(text)
    print("\nwrote", len(files), "files to", OUT)
    print("\nverification log:")
    for row in VERIFY_LOG:
        print("  ", " | ".join(row))


if __name__ == "__main__":
    main()
