import html
import importlib
import json
import os
import re
import tempfile
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from standards import STANDARDS, RESOLVED_ON, CONNECTOR
from hl import highlight
from sessions_a import SESSIONS_A
from session06 import SESSION06
from sessions_b import SESSIONS_B
from sessions_c import SESSIONS_C

# session 6, the Mondrian, was added in October 2026 and lives in its own file
SESSIONS = sorted(SESSIONS_A + [SESSION06] + SESSIONS_B + SESSIONS_C, key=lambda s: s["num"])
# Paths are relative to this file, so the repo runs from wherever it is cloned.
# The pages live in the repo root, one level up from build/.
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.environ.get("BVC_OUT", ROOT)
VERSION = "15"
REPO = "robofun-beginner-fall2026"
PUBLISHED = "2026-09-12"
TMP = os.environ.get("BVC_TMP",
                     os.path.join(tempfile.gettempdir(), "bvc_beginner_build"))

os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

# ------------------------------------------------------------------ code colors
# The hues VS Code's light theme gives Python tokens, each darkened until it clears
# 7:1 contrast on the white code background (WCAG AAA for body text), so the code
# reads when it is projected in a room with the lights on. The same colors print.
CODE_BG = "#FFFFFF"
CODE_INK = "#1F1F1F"
CODE_COLORS = {
    "hk": "#8A00B0",  # control words: if, for, while, return, import
    "hs": "#0000FF",  # def, True, False, None, and, or, not, in, is, the f of an f-string
    "hf": "#6A4E14",  # functions and methods
    "hc": "#135C70",  # classes, types, modules
    "hv": "#001080",  # variables and parameters
    "hn": "#00579A",  # CAPITAL constants
    "hq": "#A31515",  # strings
    "he": "#B00000",  # escapes inside strings
    "hd": "#035F3E",  # numbers
    "hm": "#006400",  # comments
}


def _luminance(hex_color):
    """Relative luminance of a #RRGGBB color, as WCAG defines it."""
    rgb = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(fg, bg):
    """WCAG contrast ratio between two #RRGGBB colors, from 1 to 21."""
    a, b = _luminance(fg), _luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


# VS Code draws a thin light-grey line down each step of indentation. On these pages
# the same lines are drawn 6px wide and dark, because a 1px light-grey line vanishes on
# a projector with the lights on. The grey clears 7:1 on white, like the code colors.
GUIDE = "#595959"
GUIDE_WIDTH = "6px"

for _cls, _hex in list(CODE_COLORS.items()) + [("ink", CODE_INK), ("guide", GUIDE)]:
    _ratio = contrast(_hex, CODE_BG)
    assert _ratio >= 7.0, "code color %s %s is only %.2f:1 on %s" % (_cls, _hex, _ratio, CODE_BG)

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


SEED_RANDOM = '''
# Installed by build/render.py so a snippet that picks at random prints the same
# run every build. The seed is set before the snippet starts, so its line numbers
# are unchanged and the page shows the program the student types.
import random as _random
_random.seed({seed})
'''


def run_snippet(code, stdin=None, timeout=30, preamble="", fname="snippet.py", seed=None):
    path = os.path.join(TMP, fname)
    with open(path, "w") as fh:
        fh.write(preamble + code + "\n")
    env = dict(os.environ)
    if stdin is not None or seed is not None:
        hook = ECHO_INPUT if stdin is not None else ""
        if seed is not None:
            hook = hook + SEED_RANDOM.format(seed=int(seed))
        with open(os.path.join(TMP, "sitecustomize.py"), "w") as fh:
            fh.write(hook)
        # Two hooks of the same size written in the same second share a bytecode
        # cache entry, and the second run would get the first run's seed. Never
        # cache the hook.
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        cache = os.path.join(TMP, "__pycache__")
        if os.path.isdir(cache):
            for name in os.listdir(cache):
                if name.startswith("sitecustomize."):
                    os.remove(os.path.join(cache, name))
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
    if num == "14":
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
                              stdin=chunk.get("stdin"), timeout=30, fname=fname,
                              seed=chunk.get("seed"))
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
.wrap{max-width:1080px; margin:0 auto}
/* prose lines stay at reading length inside the wider column; code gets the width */
p,li{max-width:72ch}
.dates,.sessionlist li,.toolbar,.legend,.exits p,.card p,.stamp,.pill{max-width:none}
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
section.extension{border-left:8px solid var(--clay)}
.chunk-no{
  font-family:'JetBrains Mono',monospace; font-size:13px; letter-spacing:.12em;
  text-transform:uppercase; color:var(--ochre); margin:0 0 8px; font-weight:700;
}
p{margin:0 0 14px}
ul,ol{margin:0 0 14px; padding-left:24px}
li{margin:0 0 8px}
.sessionlist li{max-width:none}
code,pre{
  /* JetBrains Mono ligatures turn != into a slashed equals and <= into a single
     glyph; students then type a character that does not exist. Keep every
     operator as the keys that produce it. */
  font-variant-ligatures:none; font-feature-settings:"liga" 0,"calt" 0,"dlig" 0;
}
code{
  font-family:'JetBrains Mono',monospace; font-size:.9em; font-weight:700;
  background:var(--code-bg); color:#1E2A2B;
  padding:2px 6px; border-radius:3px;
}
pre{
  /* 19px, a little over the 18px prose, so code reads from the back of the room */
  font-family:'JetBrains Mono',monospace; font-size:19px; line-height:1.6;
  background:var(--code-bg); color:var(--ink); border:2px solid var(--rule);
  border-left:6px solid #B9AF96; border-radius:4px;
  padding:16px 18px; overflow-x:auto; margin:0 0 16px; font-weight:500;
}
pre code{background:none; padding:0; border-radius:0; font-size:inherit; font-weight:inherit; color:inherit}
/* Python code, colored the way VS Code's light theme colors it, on white. Each color
   clears 7:1 on white (render.py checks), and the same colors print. Color only, never
   bold or italic, so every character keeps its width. */
pre.py{background:CODE_BG_HEX; color:CODE_INK_HEX}
CODE_COLOR_RULES
/* Indent guides on every code block, the lines VS Code draws down each step of
   indentation, so even a line shown on its own shows how far in it goes. Each
   four-space step is one box with a thick dark bar down its left edge. The box holds
   the step's four spaces, or on a blank line one space drawn by the CSS and not part
   of the text, so it is exactly as tall as a line wherever it sits and the bars join
   up from line to line. The spaces never wrap, even where the printed worksheets let
   code wrap. A border rather than a shadow, so the bars print. */
pre.py .ig{
  display:inline-block; width:4ch; vertical-align:top; white-space:pre;
  border-left:GUIDE_WIDTH solid GUIDE_HEX;
}
pre.py .ig:empty::before{content:" "}
pre.anatomy{background:#FFFDF7; border-left:6px solid var(--teal)}
pre.anatomy .cond{background:#FBF2DC; border-bottom:3px solid var(--ochre-line); padding:1px 2px}
pre.anatomy .blk{background:#E8F1E9; border-left:3px solid var(--green); padding:1px 2px}
pre.anatomy .nm{background:#E3EDEE; border-bottom:3px solid var(--teal); padding:1px 2px}
pre.anatomy .arg{background:#F7E4E1; border-bottom:3px solid var(--clay); padding:1px 2px}
pre.anatomy .lbl{color:var(--ink-soft); font-weight:700}
pre.anatomy .lbl-n{color:var(--teal)}
pre.anatomy .lbl-a{color:var(--clay)}
.legend i.n{background:#E3EDEE; border-bottom:3px solid var(--teal)}
.legend i.a{background:#F7E4E1; border-bottom:3px solid var(--clay)}
pre.anatomy .lbl-c{color:var(--ochre)}
pre.anatomy .lbl-b{color:var(--green)}
.legend{display:flex; flex-wrap:wrap; gap:10px 22px; font-size:16px; margin:0 0 16px}
.legend span{display:inline-flex; align-items:center; gap:8px; margin-right:18px}
.legend i{display:inline-block; width:22px; height:16px; border-radius:2px; margin-right:8px}
.legend i.c{background:#FBF2DC; border-bottom:3px solid var(--ochre-line)}
.legend i.b{background:#E8F1E9; border-left:3px solid var(--green)}
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
button.rev.hint{background:var(--card); color:var(--ochre); border:2px solid var(--ochre-line); margin:0 10px 10px 0}
button.rev.hint:hover{background:var(--ochre-tint)}
.hints .ans{margin:0 0 12px; padding-top:10px; border-top:2px solid var(--ochre-line)}
.ladder .ans{margin:12px 0 0; padding-top:12px; border-top:2px solid var(--ochre-line)}
.ladder .ans p{margin:0 0 12px}
.ladder .ans pre{margin:0 0 12px}
.ladder .q b{color:var(--clay)}
.sofar,.whole{margin:0 0 16px}
.sofar .ans,.whole .ans{margin-top:12px; padding-top:0; border-top:0}
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
  max-width:1080px; margin:0 auto; padding:8px 22px 34px;
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
.toolbar{display:flex; gap:12px; flex-wrap:wrap; margin:0 0 20px}
a.btn{
  display:inline-block; font-family:'DM Sans',sans-serif; font-size:17px; font-weight:700;
  background:var(--teal); color:#FFFDF7; text-decoration:none; border-radius:4px;
  padding:12px 20px; border:2px solid var(--teal);
}
a.btn:hover{background:var(--teal-deep)}
a.btn.quiet{background:var(--card); color:var(--teal)}
a.btn.quiet:hover{background:#EFE9DA}
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
@media (max-width:760px){
  pre{font-size:15px}
  /* a wide table scrolls inside itself instead of widening the page */
  table{display:block; overflow-x:auto; max-width:100%}
  table tbody{display:table; width:100%}
}
@media print{
  body{background:#fff; font-size:11pt}
  header.top{background:#fff; color:#111; border-bottom:3px solid #111}
  header.top h1,header.top .sub,header.top .eyebrow,.pill b{color:#111}
  .pill{border-color:#666}
  footer,.pager,details.teacher{background:#fff}
  section,.stamp,.card{background:#fff; break-inside:avoid}
  .noprint,.toolbar{display:none}
  a{color:#111}
  /* printed code keeps its old size, so printed pages and PDFs do not reflow */
  pre{font-size:15.5px}
  pre.py{background:#fff; border:1px solid #999}
}
"""

CSS = (CSS.replace("CODE_BG_HEX", CODE_BG).replace("CODE_INK_HEX", CODE_INK)
       .replace("GUIDE_HEX", GUIDE).replace("GUIDE_WIDTH", GUIDE_WIDTH)
       .replace("CODE_COLOR_RULES", " ".join("pre.py .%s{color:%s}" % kv for kv in CODE_COLORS.items())))

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


def page(title, body, hub_label="Course home", head_extra=""):
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>' + html.escape(title) + '</title>\n'
        + FONTS + '\n<style>' + CSS + '</style>\n' + head_extra + '</head>\n<body>\n'
        + body +
        '\n<script>' + JS + '</script>\n</body>\n</html>\n'
    )


def link(slug):
    return slug + ".html?v=" + VERSION


def code_block(code, context=None):
    """A block of Python, colored the way VS Code colors it.

    context is the whole program when code is only the part being added, so a name
    is colored by what it is in the whole program. Output boxes (out_block) and the
    expected/got sheets stay plain: they are not code.
    """
    return '<pre class="py"><code>' + indent_guides(highlight(code, context)) + '</code></pre>'


def indent_guides(colored):
    """Put each four-space step of indentation in its own guide span.

    colored is code that hl.py has colored, one line of code per line of text. Each
    step's four spaces go inside <span class="ig">, which the CSS draws as a thick
    bar down its left edge: the indent guides VS Code shows. A blank
    line inside an indented block gets empty guide spans, as many steps as the lines
    above and below it share, so the bars run through it unbroken the way they do in
    VS Code. The spaces stay spaces and nothing is added to the text, so code copied
    from a page pastes with its indentation as it was.
    """
    lines = colored.split("\n")
    steps = [(len(ln) - len(ln.lstrip(" "))) // 4 if ln.strip() else None for ln in lines]
    out = []
    for i, ln in enumerate(lines):
        n = steps[i]
        if n is None:
            above = next((s for s in reversed(steps[:i]) if s is not None), 0)
            below = next((s for s in steps[i + 1:] if s is not None), 0)
            out.append('<span class="ig"></span>' * min(above, below) + ln)
        else:
            out.append('<span class="ig">    </span>' * n + ln[4 * n:])
    return "\n".join(out)


def strip_block(text, width=24):
    """The ledger card's reference strip: code in the left column, a plain gloss in the right.

    Only the code column is colored. The gloss is English, so its words stay in ink
    rather than being read as keywords.
    """
    lines = []
    for ln in text.split("\n"):
        code, gloss = ln[:width], ln[width:]
        lines.append(highlight(code) + html.escape(gloss, quote=False))
    return '<pre class="py"><code>' + "\n".join(lines) + '</code></pre>'


def out_block(text, label="What actually happens"):
    return ('<p class="outlabel">' + label + '</p><pre class="out">'
            + html.escape(text) + '</pre>')


def nest_hints(idx, hints, inner, prefix="-hint", word="Hint"):
    """Wrap inner (a button and its block) in hints that open one inside the next.

    Hint 2's button sits inside hint 1's box, hint 3's inside hint 2's, and inner,
    which is usually the button that shows the answer, sits inside the last hint. So
    the hints come out in order, and the answer cannot be opened before the hints.
    With one hint, its button reads "Show a hint" rather than "Hint 1".
    """
    if not hints:
        return inner
    if isinstance(hints, str):
        hints = [hints]
    for n in range(len(hints), 0, -1):
        hid = idx + prefix + str(n)
        low = word.lower()
        if len(hints) == 1:
            show, hide = "Show a " + low, "Hide the " + low
        else:
            show, hide = word + " " + str(n), "Hide " + low + " " + str(n)
        inner = ('<button class="rev hint" data-target="' + hid + '" aria-controls="' + hid + '" '
                 'aria-expanded="false" data-show="' + show + '" data-hide="' + hide + '">'
                 + show + '</button>'
                 '<div class="ans" id="' + hid + '">' + hint_html(hints[n - 1]) + inner + '</div>')
    return '<div class="hints">' + inner + '</div>'


def hint_html(h):
    """A hint is a string of HTML, or a dict with "text" and/or "code"."""
    if isinstance(h, str):
        return '<p>' + h + '</p>'
    out = ""
    if h.get("text"):
        out += '<p>' + h["text"] + '</p>'
    if h.get("code"):
        out += code_block(h["code"])
    return out


def toggle(idx, show, hide, inner):
    """One button that opens one block."""
    return ('<button class="rev" data-target="' + idx + '" aria-controls="' + idx + '" '
            'aria-expanded="false" data-show="' + show + '" data-hide="' + hide + '">'
            + show + '</button><div class="ans" id="' + idx + '">' + inner + '</div>')


def ladder(idx, question, hints, answer_html, label="What goes next?",
           show="Show the lines", hide="Hide the lines"):
    """A question for the room, with hints that open one inside the next.

    Hint 2's button sits inside hint 1's box, hint 3's inside hint 2's, and the button
    that shows the answer sits inside the last hint, so the hints come out in order and
    nothing below the question is on screen until it is asked for.
    """
    inner = toggle(idx + "-lines", show, hide, answer_html)
    return ('<div class="predict ladder"><p class="q"><b>' + label + '</b> ' + question + '</p>'
            + nest_hints(idx, hints, inner, prefix="-h") + '</div>')


def check_step(step, code, tag):
    """A step's line must be in the chunk's program, at the line number its label names.

    The label is "Line 7", "Lines 18, 21, and 24", or "Lines 9 to 13"; every number in
    it is checked against the program, so a label cannot drift from the code.
    """
    lines = code.split("\n")
    wanted = [ln for ln in step["line"].split("\n") if ln.strip()]
    for ln in wanted:
        assert ln in lines, "%s: step line not in the program: %r" % (tag, ln)
    label = step["label"]
    m = re.fullmatch(r"Lines (\d+) to (\d+)", label)
    if m:
        nums = list(range(int(m.group(1)), int(m.group(2)) + 1))
        assert [lines[n - 1] for n in nums] == wanted, "%s: %s does not match" % (tag, label)
        return
    nums = [int(x) for x in re.findall(r"\d+", label)]
    assert nums, "%s: step label needs a line number: %r" % (tag, label)
    for n in nums:
        assert lines[n - 1] in wanted, "%s: %s names line %d, which is %r" % (tag, label, n, lines[n - 1])


def line_ladders(tag, program, steps, start=None, whole="Show the whole program"):
    """One question per new line of a program, each behind a ladder of hints.

    The program so far sits behind a button, then each step is a What goes next?
    ladder whose last button shows the line, then the whole program sits behind a
    button. Every step's line is checked against the program at the line its label
    names, so a label cannot drift from the code.
    """
    out = []
    if start:
        out.append('<div class="sofar">' + toggle(tag + "-start", "Show the program so far",
                   "Hide the program so far", code_block(start)) + '</div>')
    for j, st in enumerate(steps):
        check_step(st, program, tag)
        sid = tag + "-l" + str(j + 1)
        ans = code_block(st["line"], context=program)
        if st.get("note"):
            ans += '<p>' + st["note"] + '</p>'
        low = st["label"][0].lower() + st["label"][1:]
        out.append(ladder(sid, st["q"], st["hints"], ans,
                          label=st["label"] + ". What goes next?",
                          show="Show " + low, hide="Hide " + low))
    out.append('<div class="whole">' + toggle(tag + "-whole", whole,
               whole.replace("Show", "Hide", 1), code_block(program)) + '</div>')
    return "".join(out)


def reveal(idx, question, answer, qlabel="Predict", extra="",
           show="Show the answer", hide="Hide the answer", hints=None):
    inner = toggle(idx, show, hide, extra + '<p>' + answer + '</p>')
    return ('<div class="predict"><p class="q">' + qlabel + ': ' + question + '</p>'
            + nest_hints(idx, hints, inner) + '</div>')


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
    label = "Bonus session" if bonus else "Session " + str(n) + " of 13"

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

    ws = s.get("worksheet")
    if ws:
        b.append('<div class="toolbar"><a class="btn" href="' + link(ws["slug"])
                 + '">Open the worksheet</a><a class="btn quiet" href="' + ws["slug"]
                 + '.pdf?v=' + VERSION + '" download>Download the worksheet (PDF)</a></div>')

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
        if q.get("code"):
            b.append(code_block(q["code"]))
        extra = code_block(q["code_a"]) if q.get("code_a") else ""
        b.append(reveal("s%d-op%d" % (n, i), q["q"], q["a"], "Question", extra))
    b.append('</section>')

    for i, ch in enumerate(s["chunks"]):
        tag = "s%d-c%d" % (n, i + 1)
        out, mode = verify(ch, tag)
        b.append('<section class="chunk"><p class="chunk-no">Chunk ' + str(i + 1)
                 + ' of ' + str(len(s["chunks"])) + '</p>')
        b.append('<h2>' + html.escape(ch["title"]) + '</h2>')
        b.append('<p>' + ch["teach"] + '</p>')
        if ch.get("figure"):
            b.append(ch["figure"])
        nx = ch.get("next")
        shown = [code_block(ch["code"], (ch.get("prefix", "") + ch["code"]) if ch.get("prefix") else None)]
        if ch.get("prefix"):
            shown.append('<p class="note">' + ch.get("where",
                     'Add this code to the file you made in chunk 3. Where it goes matters. '
                     'Functions are defined near the top of a program, after the imports and '
                     'before any line that does work. The new function is separate from '
                     '<code>step_end</code>: it starts with its own <code>def</code> at the '
                     'left edge, not indented. Put it after the <code>return</code> line that '
                     'ends <code>step_end</code>, leave one blank line between them, and keep '
                     'it before <code>pygame.init()</code>. Put the lines that call the function '
                     'under the comment <code># ---- your drawing, done once ----</code>. '
                     'That is after <code>canvas.fill(BG)</code>, so the canvas exists before '
                     'you draw on it, and before <code>while running:</code>, because the loop '
                     'only shows what was drawn before it started. Then run the whole file.') + '</p>')
        steps = ch.get("steps")
        if steps:
            start = ch["start"] if "start" in ch else s["chunks"][i - 1]["code"]
            b.append(line_ladders(tag, ch["code"], steps, start))
            b.extend(shown[1:])  # the note saying where the lines go, when there is one
        elif nx:
            b.append(ladder(tag + "-next", nx["q"], nx["hints"],
                            "".join(shown) + '<p>' + nx["a"] + '</p>'))
        else:
            b.extend(shown)
        loops = "while running" in ch["code"]
        extra = ""
        if out:
            lbl = "What it actually prints"
            if ch.get("seed") is not None:
                lbl = "What it actually prints, on one run"
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
        if ch.get("code_a"):
            extra = extra + code_block(ch["code_a"])
        if ch.get("figure_a"):
            extra = extra + ch["figure_a"]
        b.append(reveal(tag, ch["predict"], ch["reveal"], "Predict", extra,
                        "Run it first, then check here", "Hide", ch.get("hint")))
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
    extra = ""
    if h.get("code"):
        b.append(code_block(h["code"]))
        out, mode = verify(h, "s%d-hinge" % n)
        if out:
            extra = out_block(out, "What it actually prints")
    if h.get("code_a"):
        extra = extra + code_block(h["code_a"])
    b.append(reveal("s%d-hinge" % n, h["q"], h["a"], "Question", extra))
    b.append('</section>')

    br = s["brief"]
    b.append('<section class="brief"><p class="chunk-no">Build &middot; '
             + str(br["minutes"]) + ' minutes</p><h2>' + html.escape(br["title"]) + '</h2>')
    if br.get("intro"):
        b.append('<p>' + br["intro"] + '</p>')
    b.append('<ol>')
    for st in br["steps"]:
        b.append('<li>' + st + '</li>')
    b.append('</ol>')
    for j, tool in enumerate(br.get("tools", [])):
        # a function written one line at a time, each line behind a hint ladder, and
        # a real run of the finished function at the end
        tag = "s%d-tool%d" % (n, j + 1)
        out, mode = verify(tool, tag)
        b.append('<h3>' + html.escape(tool["title"]) + '</h3>')
        if tool.get("intro"):
            b.append('<p>' + tool["intro"] + '</p>')
        b.append(line_ladders(tag, tool["code"], tool["steps"], tool.get("start"),
                              whole="Show the whole function and its test"))
        if out:
            b.append(reveal(tag, tool["predict"], tool["reveal"], "Predict",
                            out_block(out, "What it actually prints"),
                            "Run it first, then check here", "Hide", tool.get("hint")))
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
            if card.get("seed") is not None:
                lbl = "What it actually prints, on one run"
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
             '<p>All three are real places to stop. Nobody is behind for finishing at the floor.</p>'
             '<div class="exits">')
    b.append('<div class="exit floor"><p class="tag">Floor</p><p>' + ex["floor"] + '</p></div>')
    b.append('<div class="exit middle"><p class="tag">Middle</p><p>' + ex["middle"] + '</p></div>')
    b.append('<div class="exit stretch"><p class="tag">Stretch</p><p>' + ex["stretch"] + '</p></div>')
    b.append('</div></section>')

    xt = s.get("extension")
    if xt:
        b.append('<section class="extension"><p class="chunk-no">Extension &middot; '
                 'for after the stretch exit</p><h2>' + html.escape(xt["title"]) + '</h2>')
        b.append(xt["intro"])
        for j, card in enumerate(xt.get("cards", [])):
            tag = "s%d-ext%d" % (n, j + 1)
            out, mode = verify(card, tag)
            b.append('<h3>' + html.escape(card["title"]) + '</h3>')
            if card.get("teach"):
                b.append('<p>' + card["teach"] + '</p>')
            if card.get("figure"):
                b.append(card["figure"])
            nx = card.get("next")
            if nx:
                b.append(ladder(tag + "-next", nx["q"], nx["hints"],
                                code_block(card["code"]) + '<p>' + nx["a"] + '</p>'))
            else:
                b.append(code_block(card["code"]))
            extra = ""
            if out:
                lbl = "What it actually prints"
                if card.get("seed") is not None:
                    lbl = "What it actually prints, on one run"
                extra = out_block(out, lbl)
            b.append(reveal(tag, card["predict"], card["reveal"], "Predict", extra,
                            "Run it first, then check here", "Hide", card.get("hint")))
        if xt.get("steps"):
            b.append('<h3>Building it</h3><ol>')
            for st in xt["steps"]:
                b.append('<li>' + st + '</li>')
            b.append('</ol>')
        if xt.get("checks"):
            b.append('<h3>Expected and got</h3>'
                     '<p>Fill in the left column before you run. Fill in the right column after.</p>')
            b.append('<table><tr><th>Expected</th><th>Got</th></tr>')
            for row in xt["checks"]:
                b.append('<tr><td>' + row + '</td><td class="fill"></td></tr>')
            b.append('</table>')
        b.append('</section>')

    xc = s.get("extras")
    if xc:
        names = xc["cards"]
        b.append('<section><h2>Finished with time left?</h2>'
                 '<p>There are three extra cards for this session: ' + html.escape(names[0])
                 + ', ' + html.escape(names[1]) + ', and ' + html.escape(names[2])
                 + '. Each card is a new program that uses only what is on this page. '
                 'Pick any one.</p>'
                 '<div class="toolbar"><a class="btn" href="' + link(xc["slug"])
                 + '">Open the extra cards</a></div></section>')

    b.append('<section><h2>Ledger card</h2><p>' + s["ledger"] + '</p>'
             '<p><a href="' + link("semester_ledger_card") + '">Open the semester ledger card</a></p></section>')

    t = s["teacher"]
    b.append('<details class="teacher"><summary>Teacher panel</summary>')
    b.append('<h3>Timing, 90 minutes</h3><ul>')
    for x in t["timing"]:
        b.append('<li>' + html.escape(x) + '</li>')
    b.append('</ul><p class="note">Pacing: most rooms will not reach the end of '
             'the build brief. The exits exist so that stopping there is a finish, not a failure.</p>')
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
    if ws:
        b.append('<h3>Files</h3><p>The worksheet covers ' + ws["covers"] + '. Print one per '
                 'student from the PDF, double-sided, US letter. <a href="' + link(ws["slug"])
                 + '">Worksheet</a> &middot; <a href="' + ws["slug"] + '.pdf?v=' + VERSION
                 + '" download>PDF</a> &middot; <a href="' + link(ws["slug"] + "_key")
                 + '">Answer key</a>. The key is linked from this panel only.</p>')
    if xc:
        if not ws:
            b.append('<h3>Files</h3>')
        b.append('<p>The extra cards are for a student who finishes the build while you are '
                 'working with someone else: three programs, 15 to 20 minutes each, that use '
                 'only what this session has taught. Every card shows a finished run, so the '
                 'student can check the work without you. The bug hunt needs the least help. '
                 + xc.get("note", "") + '<a href="' + link(xc["slug"]) + '">Extra cards</a> '
                 '&middot; <a href="' + link(xc["slug"] + "_key") + '">Answer key</a>. The key '
                 'is linked from this panel only.</p>')
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
                 'starting in session 6.</p></section>')

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
             '110 West End Avenue. The Monday and Friday sections cover the same thirteen sessions.</p>'
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
    b.append('<p class="sub">Thirteen sessions of ninety minutes. You read the code, '
             'trace it out loud, and then run it. Monday and Friday are separate classes '
             'working through the same thirteen sessions.</p>')
    b.append('<div class="dates">'
             '<span class="pill"><b>Monday</b> Sep 14 to Dec 14, 13 sessions, last date to be decided</span>'
             '<span class="pill"><b>Friday</b> Sep 18 to Dec 18, 13 sessions</span>'
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
             'all real places to stop. One stamp goes on the semester card.</li>'
             '</ol></section>')

    b.append('<section><h2>The thirteen sessions</h2><ul class="sessionlist">')
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
    b.append('<div class="card"><h3>Monday, 13 sessions</h3><table>'
             '<tr><th>Date</th><th>Session</th></tr>')
    for s in SESSIONS:
        if s.get("bonus"):
            continue
        b.append('<tr><td>' + s["mon"] + '</td><td>' + str(s["num"]) + '. '
                 + html.escape(s["title"]) + '</td></tr>')
    b.append('</table></div>')
    b.append('<div class="card"><h3>Friday, 13 sessions</h3><table>'
             '<tr><th>Date</th><th>Session</th></tr>')
    fri = sorted(SESSIONS, key=lambda s: ("Dec" in s["fri"], s["fri"]))
    order = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    by_num = {s["num"]: s for s in SESSIONS}
    for num in order:
        s = by_num[num]
        tag = "Bonus. " if s.get("bonus") else str(s["num"]) + ". "
        b.append('<tr><td>' + s["fri"] + '</td><td>' + tag + html.escape(s["title"])
                 + '</td></tr>')
    b.append('</table></div></div>')
    b.append('<p class="note">The course is thirteen sessions since session 6, the Mondrian, was '
             'added in October. Monday has twelve dates between Sep 14 and Dec 14, so the last '
             'Monday session, the demo, needs a date after Dec 14 or a session merged into '
             'another; that date is still to be decided. Friday has thirteen dates, so every '
             'Friday session has one, and the bonus session is no longer scheduled. It stays on '
             'the site for anyone who wants it. If a parent compares the two classes, the '
             'required content is identical.</p>'
             '<p class="note">From session 4 on, Friday runs one to two sessions ahead of '
             'Monday, so in most weeks the two sections are on different pages. Each page '
             'shows both dates in its header.</p>')
    b.append('</section>')

    b.append('<section><h2>Machines and libraries</h2>'
             '<p>VS Code on the desktop, throughout. One graphics library, pygame, from '
             'session 6 onward, installed with <code>pip install pygame</code>. There is no '
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
             '<tr><td><code>return</code></td><td>Session 5</td><td>Without it a function '
             'cannot be composed, tested, or reused, and every function returns '
             '<code>None</code>.</td></tr>'
             '<tr><td><code>and</code>, <code>or</code></td><td>Session 2</td><td>With '
             'nesting banned there was no way to write two conditions at once.</td></tr>'
             '<tr><td><code>len</code>, <code>sum</code>, <code>max</code>, <code>min</code></td>'
             '<td>Session 3</td><td>Taught as the reveal after the hand-written version, '
             'never before it.</td></tr>'
             '<tr><td>String methods and slicing</td><td>Session 8</td><td>Students could '
             'not clean their own input, which forced capitals-and-spaces workarounds.</td></tr>'
             '<tr><td>Dictionaries</td><td>Session 10</td><td>The parallel-list failure is '
             'taught first, then the fix.</td></tr>'
             '<tr><td><code>.find()</code></td><td>Session 9</td><td>Revealed after the '
             'hand-written rack scan.</td></tr>'
             '<tr><td>pygame from session 6 onward</td><td>Session 6</td><td>The only graphics library in the course. It replaces the turtle drawing session, which does not run in VS Code.</td></tr>'
             '<tr><td>KEYDOWN, mouse, frame timers</td><td>Session 12</td><td>Without them a '
             'game reads as a demo. A held key and a single press are different '
             'questions.</td></tr>'
             '<tr><td><code>random.seed</code>, <code>randint</code></td><td>Session 3</td>'
             '<td>A seed is how you test a program that is supposed to be '
             'unpredictable.</td></tr>'
             '</table></section>')

    b.append('<section><h2>Still excluded, all thirteen sessions</h2>'
             '<ul>'
             '<li><b>Nested gates.</b> Flat <code>if</code>, <code>elif</code>, '
             '<code>else</code> only. If a student reaches for an if inside an if, hand them '
             '<code>and</code>.</li>'
             '<li><b><code>break</code> and <code>continue</code>.</b> Every '
             '<code>while</code> has a stopping condition you can point at.</li>'
             '<li><b><code>while True</code>.</b> Same reason.</li>'
             '<li><b><code>try</code> and <code>except</code>.</b> Ask-until-valid loops '
             'cover the same ground at this level.</li>'
             '<li><b><code>//</code>.</b> A single slash and <code>%</code> are enough.</li>'
             '<li><b><code>class</code>.</b> Advanced course material.</li>'
             '<li><b>Recursion, list comprehensions, lambda, <code>global</code>.</b></li>'
             '<li><b>Multi-file programs and importing your own module.</b> Advanced '
             'course.</li>'
             '<li><b>File input and output.</b> Held as a float, not one of the thirteen sessions.</li>'
             '<li><b><code>pygame.font</code>.</b> Words go in the terminal and visuals go '
             'in the window. That split holds all term.</li>'
             '<li><b>turtle.</b> Not used anywhere in this course. It needs a library our '
             'VS Code setup does not have, so pygame does all of the drawing, starting in '
             'session 6. No turtle program appears in this repo.</li>'
             '</ul></section>')

    b.append('<section><h2>The frame loop, and only this one</h2>'
             '<p>This course uses one frame loop, everywhere, with no exceptions. Students '
             'first copy it in session 6 as a loop holding '
             'a finished drawing on screen, and session 11 takes it apart.</p>')
    b.append(code_block('running = 1\nwhile running:\n    for event in pygame.event.get():\n'
                        '        if event.type == pygame.QUIT:\n            running = 0\n'
                        '    screen.fill(BG)\n    # draw here\n    pygame.display.flip()\n'
                        '    clock.tick(60)\npygame.quit()'))
    b.append('<p>A window never closes itself. It closes when the person closes it. Any '
             'program handed out in this course has this shape.</p>'
             '<p>Two placements of the drawing, both legitimate, and students meet them in '
             'this order. In session 6 the drawing is done once onto a '
             '<code>pygame.Surface</code> above the loop, and the loop only blits it, '
             'because the picture never changes. From session 11 on, the '
             '<code>fill</code> and the drawing sit inside the loop, because the picture '
             'changes every frame.</p></section>')

    b.append('<section><h2>Standing rules</h2><ul>'
             '<li><b>One change per run.</b> Change one thing, run it, write down what '
             'happened.</li>'
             '<li><b>Predict before you run.</b> Out loud or on paper, every chunk.</li>'
             '<li><b>Expected and got.</b> The expected column is filled in before the run, '
             'not after.</li>'
             '<li><b>Names that say what they do.</b> A function called <code>check</code> that removes a '
             'life gets renamed. This is an exit criterion, not a style preference.</li>'
             '<li><b>Words in the terminal, visuals in the window.</b></li>'
             '<li><b>Functions at the top.</b> Every <code>def</code> goes together near the top of the file, after the imports and before any line that does work. Python must read a function before the line that calls it.</li>'
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
             '<li>Session 13 reads the card out loud. If a stamp is unreadable, that is the '
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
    b.append(strip_block(
        'name = value            a variable: store a value under a name\n'
        'type(value)             str for text, int for a whole number\n'
        'int(text)               text to number, on its own line\n'
        'f"{name} has {n}"       drop values into a sentence\n'
        'if / elif / else        flat gates, never nested\n'
        '==  !=  <  >  <=  >=    comparisons, give True or False\n'
        'and / or                two conditions at once\n'
        'while condition:        repeats while True; the condition is what stops it\n'
        'for i in range(5):      0 1 2 3 4, stops before 5\n'
        'list[0]                 first slot; last is len - 1\n'
        'text[0:3]               slots 0 1 2, stops before 3\n'
        'def f(x):               ...    return x * 2\n'
        'no return               returns None\n'
        'd = {"key": value}      look up with d["key"]\n'
        'key in d                True or False, checks keys\n'
        'a % b                   remainder; wraps a counter\n'
        'rack.find(ch)           a slot, or -1 for not found\n'
        '360 / sides             the turn that closes a shape\n'
        'math.radians(deg)       convert before cos and sin\n'
        'cos is across, sin down the far end of a step\n'
        'draw.rect(c, col, r, 10)  r is (x, y, w, h); the 10 makes a border\n'
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

    # Worksheets live in wsNN.py and import this module as render. Point that name at
    # the running script, so they share its sessions and run log rather than loading a
    # second copy of it.
    sys.modules.setdefault("render", sys.modules[__name__])
    for s in SESSIONS:
        ws = s.get("worksheet")
        if not ws:
            continue
        mod = importlib.import_module("ws%02d" % s["num"])
        sheet_fn = getattr(mod, "worksheet%02d" % s["num"])
        key_fn = getattr(mod, "worksheet%02d_key" % s["num"])
        label = "Session " + str(s["num"]) + " worksheet"
        files[ws["slug"] + ".html"] = page(label + ": " + mod.TITLE + " | Beyond Vibe Coding beginner",
                                          sheet_fn(), head_extra=mod.HEAD)
        files[ws["slug"] + "_key.html"] = page(label + ", answer key | Beyond Vibe Coding beginner",
                                              key_fn(), head_extra=mod.HEAD)
        print("rendered", ws["slug"], "and its key")

    # Extra cards live in extras.py, which imports this module the same way.
    for s in SESSIONS:
        xc = s.get("extras")
        if not xc:
            continue
        extras = importlib.import_module("extras")
        label = "Session " + str(s["num"]) + " extra cards"
        files[xc["slug"] + ".html"] = page(label + " | Beyond Vibe Coding beginner",
                                          extras.cards_page(s), head_extra=extras.HEAD)
        files[xc["slug"] + "_key.html"] = page(label + ", answer key | Beyond Vibe Coding beginner",
                                              extras.key_page(s), head_extra=extras.HEAD)
        print("rendered", xc["slug"], "and its key")

    for name, text in files.items():
        with open(os.path.join(OUT, name), "w") as fh:
            fh.write(text)
    print("\nwrote", len(files), "files to", OUT)
    print("\nverification log:")
    for row in VERIFY_LOG:
        print("  ", " | ".join(row))


if __name__ == "__main__":
    main()
