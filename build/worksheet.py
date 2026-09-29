"""Shared parts of every session worksheet: the worksheet CSS, the blocks, the typing script.

These are the Advanced Python course's worksheet helpers (its build/ws01.py), brought
into this repo so the beginner sheets look the same. Every beginner sheet imports them
from here rather than copying them. Additions, all with defaults that keep the original
behaviour: trace_table takes the name of its index column (a Boolean table counts
riders, not loop passes) and optional column widths, and run_table takes the label of
its first column. Trace and run tables switch off ligatures, as code blocks do, because
their headings quote conditions such as answer != "yes".

A sheet module (ws02.py for session 2) writes worksheetNN() and worksheetNN_key();
render.py writes both pages with WS_CSS added to the head.
"""

import html

import render

WS_CSS = """
<style>
.ws-name{display:flex; gap:24px; flex-wrap:wrap; font-size:17px; margin:0 0 6px}
.ws-name span{flex:1 1 220px; border-bottom:2px solid var(--ink); padding:0 0 4px}
.ws-name b{font-family:'JetBrains Mono',monospace; font-size:12.5px; letter-spacing:.1em;
  text-transform:uppercase; color:var(--ochre); margin-right:8px}
.fname{font-family:'JetBrains Mono',monospace; font-size:12.5px; letter-spacing:.1em;
  text-transform:uppercase; color:var(--ink-soft); margin:0 0 6px; font-weight:700}
.lines p{border-bottom:2px solid var(--rule); min-height:34px; margin:0 0 10px; padding:0 0 2px}
.key{background:var(--green-tint); color:var(--green-ink)}
[contenteditable="true"]{cursor:text; outline:none; min-height:1.4em}
[contenteditable="true"]:focus{background:var(--ochre-tint); box-shadow:inset 0 0 0 3px var(--ochre-line)}
[contenteditable="true"]:empty::before{content:attr(data-hint); color:#B9AF96; font-weight:400}
table.trace td[contenteditable="true"]{font-size:19px; font-weight:700; color:var(--green-ink)}
table.rename td[contenteditable="true"],.lines p[contenteditable="true"]{font-size:18px; color:var(--green-ink); text-align:left}
.lines p[contenteditable="true"]{min-height:38px; padding:4px 8px}
.livebar{display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin:0 0 20px; padding:12px 16px;
  border:2px dashed var(--teal); border-radius:5px; background:var(--card)}
.livebar p{margin:0; font-size:16px}
.livebar button{font-family:'DM Sans',sans-serif; font-size:15px; font-weight:700; background:var(--card);
  color:var(--teal); border:2px solid var(--rule); border-radius:4px; padding:8px 14px; cursor:pointer}
.livebar button:hover{background:#EFE9DA}
@media print{.livebar{display:none} [contenteditable="true"]:empty::before{content:none}
  [contenteditable="true"]{color:var(--ink)}}
.lines p.key{min-height:0; padding:8px 10px; border-bottom:0; border-left:4px solid var(--green)}
table.trace{table-layout:fixed}
/* the headings quote conditions such as answer != "yes"; keep != as the two keys that type it */
table.trace,table.rename{font-variant-ligatures:none; font-feature-settings:"liga" 0,"calt" 0,"dlig" 0}
table.trace th{font-family:'JetBrains Mono',monospace; text-align:center; font-size:14.5px;
  padding:6px 3px; white-space:normal; overflow-wrap:normal}
table.trace td{height:36px; text-align:center; font-family:'JetBrains Mono',monospace; font-size:15px;
  vertical-align:middle}
table.trace td.i{background:#EFE9DA; font-weight:700}
table.trace tr.start td{background:#FBF9F3; color:var(--ink-soft)}
table.trace tr.done td{background:#E8F1E9; color:var(--green-ink)}
table.trace tr.done td.i{background:#D9E7DC}
table.trace tr.done td.q{background:#E8F1E9}
table.trace th.q,table.trace td.q{background:#FBF2DC}
table.rename td{height:38px}
table.rename td.old{font-family:'JetBrains Mono',monospace; font-weight:700; width:130px; text-align:center;
  background:#EFE9DA; white-space:nowrap}
.two-up{display:grid; gap:18px; grid-template-columns:minmax(0,1fr)}
.two-up pre{margin:0; font-size:14px; line-height:1.5}
.nb{font-size:15px; color:var(--ink-soft)}
.tscroll{overflow-x:auto; margin:0 0 16px}
.tscroll table{margin:0}
@media (max-width:760px){
  main{padding:22px 16px 8px} header.top{padding:24px 16px 20px} section{padding:18px 16px}
  /* on a phone a table keeps its width and scrolls inside its own box, so True and
     False never break in the middle; the page itself does not scroll sideways */
  table.trace{min-width:560px} table.rename{min-width:520px}
  th,td{padding:7px 8px}
  table.trace th{font-size:12.5px} table.trace td{font-size:14px}
}
@media print{.tscroll{overflow:visible; margin:0 0 12px}}
@media print{
  @page{size:letter; margin:14mm 14mm 16mm}
  body{font-size:12pt; line-height:1.5} main{padding:0}
  header.top{padding:8px 0 6px; margin-bottom:10px}
  header.top .dates,header.top .sub{display:none} header.top h1{font-size:21pt; margin:0 0 6px}
  nav.pager,footer,.toolbar{display:none}
  .ws-name{font-size:12pt; margin:0 0 10px}
  section{padding:14px 16px; margin:0 0 12px; border-width:1.5px; break-inside:auto}
  pre,tr,p,.lines p{break-inside:avoid} h2,h3,.chunk-no{break-after:avoid}
  pre{white-space:pre-wrap; overflow-wrap:anywhere}
  thead{display:table-header-group} .keep{break-inside:avoid} table.trace,table.rename{break-inside:avoid}
  .two-up{grid-template-columns:minmax(0,1fr); gap:8px}
  .chunk-no{margin:0 0 4px; font-size:9.5pt} h2{font-size:19pt; margin:0 0 8px} h3{font-size:14pt}
  table{font-size:12pt} table.trace th{font-size:10.5pt; padding:4px 3px}
  table.trace td{height:34px; font-size:12pt; padding:3px 6px}
  table.rename td{height:42px} .lines p{min-height:32px; margin:0 0 12px}
  .nb{font-size:11.5pt} code{font-size:.92em}
  .two-up pre{font-size:10.5pt; line-height:1.5; border:1px solid #999; padding:10px 14px}
  .ws-name span{border-bottom-color:#111}
}
</style>
"""

KEY = {"on": False}


def esc(s):
    """Escape text for HTML, leaving quote marks as they are."""
    return html.escape(s, quote=False)


def code(text, label=None):
    """Return a labelled code block, built the same way as the session pages' code blocks."""
    out = "<div>"
    if label:
        out += f'<p class="fname">{esc(label)}</p>'
    return out + render.code_block(text) + "</div>"


def lines(n, answer=None):
    """Return n ruled writing lines, or the answer in the key version."""
    if KEY["on"] and answer:
        return f'<div class="lines"><p class="key">{answer}</p></div>'
    return '<div class="lines">' + "<p></p>" * n + "</div>"


def trace_table(headers, start, rows, given, q_cols=(), done=None, index="i", widths=None):
    """Return a hand-trace table.

    headers: column names. start: values for the row before the loop, or None.
    rows: list of index values. given: dict column -> function(i) for cells the
    worksheet fills in for the student. q_cols: columns tinted as True/False or
    yes/no questions. done: dict row -> list of values for the worked rows.
    index: the header of the numbering column (i for a loop, rider for a table of riders).
    widths: optional column widths in percent, so a long printed line fits on one row.
    """
    out = '<table class="trace">'
    if widths:
        assert len(widths) == len(headers) and sum(widths) == 100
        out += "<colgroup>" + "".join(f'<col style="width:{w}%">' for w in widths) + "</colgroup>"
    out += "<thead><tr>"
    for h in headers:
        cls = ' class="q"' if h in q_cols else ""
        out += f"<th{cls}>{esc(h)}</th>"
    out += "</tr></thead>"
    if start is not None:
        out += '<tr class="start">'
        for h, v in zip(headers, start):
            out += f"<td>{esc(str(v))}</td>"
        out += "</tr>"
    done = done or {}
    for i in rows:
        if i in done:
            out += '<tr class="done">'
            for h, v in zip(headers, done[i]):
                cls = ' class="i"' if h == index else (' class="q"' if h in q_cols else "")
                out += f"<td{cls}>{esc(str(v))}</td>"
            out += "</tr>"
            continue
        out += "<tr>"
        for h in headers:
            if h == index:
                out += f'<td class="i">{i}</td>'
            elif h in given:
                out += f"<td>{esc(str(given[h](i)))}</td>"
            elif h in q_cols:
                out += '<td class="q"></td>'
            else:
                out += "<td></td>"
        out += "</tr>"
    return '<div class="tscroll">' + out + "</table></div>"


def rename_table(names, answers=None):
    """Return the three-column rename table, filled in for the key version."""
    out = ('<table class="rename"><tr><th>Old name</th><th>What the value is, in words</th>'
           "<th>Clearer new name</th></tr>")
    for n in names:
        if KEY["on"] and answers and n in answers:
            what, new = answers[n]
            out += (f'<tr><td class="old">{esc(n)}</td><td class="key">{esc(what)}</td>'
                    f'<td class="key"><code>{esc(new)}</code></td></tr>')
        else:
            out += f'<tr><td class="old">{esc(n)}</td><td></td><td></td></tr>'
    return '<div class="tscroll">' + out + "</table></div>"


def run_table(rows, label="Line"):
    """Return the predicted-against-printed table; the key shows what prints."""
    out = (f'<table class="rename"><tr><th>{esc(label)}</th><th>What I predicted</th>'
           "<th>What it printed</th><th>Right?</th></tr>")
    for name, printed in rows:
        cell = f'<td class="key"><code>{esc(printed)}</code></td>' if KEY["on"] else "<td></td>"
        out += f'<tr><td class="old">{esc(name)}</td><td></td>{cell}<td></td></tr>'
    return '<div class="tscroll">' + out + "</table></div>"


LIVE_JS = """
<script>
(function(){
  var blanks = [];
  document.querySelectorAll('table.trace td, table.rename td, .lines p').forEach(function(el){
    if (el.classList.contains('i') || el.classList.contains('old')) return;
    if (el.closest('tr.done') || el.closest('tr.start')) return;
    if (el.textContent.trim() !== '') return;
    el.setAttribute('contenteditable', 'true');
    el.setAttribute('tabindex', '0');
    el.setAttribute('data-hint', el.tagName === 'P' ? 'type here' : '');
    blanks.push(el);
  });
  document.addEventListener('keydown', function(e){
    var el = document.activeElement;
    if (!el || el.getAttribute('contenteditable') !== 'true') return;
    if (e.key === 'Enter' || (e.key === 'Tab' && !e.shiftKey)) {
      if (e.key === 'Enter' && el.tagName === 'P' && e.shiftKey) return;
      e.preventDefault();
      var i = blanks.indexOf(el);
      if (i >= 0 && i + 1 < blanks.length) blanks[i + 1].focus();
    }
    if (e.key === 'Tab' && e.shiftKey) {
      e.preventDefault();
      var j = blanks.indexOf(el);
      if (j > 0) blanks[j - 1].focus();
    }
  });
  var clear = document.getElementById('clearall');
  if (clear) clear.addEventListener('click', function(){
    if (!confirm('Clear everything typed on this page?')) return;
    blanks.forEach(function(el){ el.textContent = ''; });
  });
})();
</script>
"""


# ------------------------------------------------------------- page furniture

def masthead(s, title, covers):
    """Return the teal band: the session page's eyebrow, the sheet's title, the date pills."""
    return (
        '<header class="top"><div class="wrap">'
        '<p class="eyebrow">Beyond Vibe Coding &middot; Beginner &middot; Session '
        + str(s["num"]) + ' of 12</p>'
        '<h1>' + esc(title) + '</h1>'
        '<div class="dates">'
        '<span class="pill"><b>Monday section</b> ' + s["mon"] + '</span>'
        '<span class="pill"><b>Friday section</b> ' + s["fri"] + '</span>'
        '<span class="pill"><b>Covers</b> ' + esc(covers) + '</span>'
        '</div></div></header>'
    )


def name_line(s):
    """Return the name and date fields, or the teacher-copy line in the key."""
    date = s["mon"] + " or " + s["fri"]
    if KEY["on"]:
        return ('<div class="ws-name"><span><b>Teacher copy</b> every slot filled; worked rows '
                'the students get are the same values</span><span><b>Date</b> ' + date
                + '</span></div>')
    return ('<div class="ws-name"><span><b>Name</b></span><span><b>Date</b> ' + date
            + '</span></div>')


def toolbar(s, slug):
    """Return the screen-only toolbar: back to the session page, and the PDF on the student sheet."""
    out = ('<div class="toolbar"><a class="btn quiet" href="' + render.link(s["slug"])
           + '">Back to the session ' + str(s["num"]) + ' page</a>')
    if not KEY["on"]:
        out += ('<a class="btn" href="' + slug + '.pdf?v=' + render.VERSION
                + '" download>Download this worksheet (PDF)</a>')
    return out + '</div>'


def livebar():
    """Return the projector typing bar; the student sheet only."""
    if KEY["on"]:
        return ""
    return ('<div class="livebar"><p><b>On the projector:</b> click any blank cell or line '
            'and type. Tab or Enter moves to the next blank. Nothing is saved when the page '
            'closes.</p><button id="clearall" type="button">Clear everything</button></div>')


def chunk_section(s, n, body):
    """Return one chunk as a card, labelled and titled exactly as on the session page."""
    ch = s["chunks"][n - 1]
    return ('<section class="chunk"><p class="chunk-no">Chunk ' + str(n) + ' of '
            + str(len(s["chunks"])) + '</p><h2>' + esc(ch["title"]) + '</h2>'
            + body + '</section>')


def brief_section(s, body):
    """Return the build brief as a card, labelled and titled exactly as on the session page."""
    br = s["brief"]
    return ('<section class="brief"><p class="chunk-no">Build &middot; ' + str(br["minutes"])
            + ' minutes</p><h2>' + esc(br["title"]) + '</h2>' + body + '</section>')


def pager(s):
    """Return the session page, course home, and next-session links."""
    nxt = [x for x in render.SESSIONS if x["num"] == s["num"] + 1][0]
    return ('<nav class="pager"><a href="' + render.link(s["slug"]) + '">&larr; Session '
            + str(s["num"]) + ': ' + esc(s["title"]) + '</a>'
            '<a href="' + render.link("beginner_semester_hub") + '">Course home</a>'
            '<a href="' + render.link(nxt["slug"]) + '">Session ' + str(nxt["num"]) + ': '
            + esc(nxt["title"]) + ' &rarr;</a></nav>')


def footer(s):
    """Return the worksheet footer (screen only)."""
    return ('<footer><div class="wrap"><p>Beyond Vibe Coding, beginner semester, Fall 2026. '
            'Worksheet for session ' + str(s["num"]) + ', written by a generator in '
            '<code>build/</code>. Every printed line in the answer key comes from running the '
            'program when the site was built.</p></div></footer>')


def sheet(s, title, covers, slug, sections):
    """Assemble a worksheet body: masthead, name line, toolbar, live bar, sections, pager."""
    b = masthead(s, title, covers)
    b += '<main><div class="wrap">'
    b += name_line(s) + toolbar(s, slug) + livebar()
    b += "".join(sections)
    b += '</div></main>' + pager(s) + footer(s)
    if not KEY["on"]:
        b += LIVE_JS
    return b


def head(print_css=""):
    """Return what a worksheet page adds to its head: WS_CSS, then the sheet's own page breaks."""
    if not print_css:
        return WS_CSS
    return WS_CSS + "<style>\n@media print{" + print_css + "}\n</style>\n"
