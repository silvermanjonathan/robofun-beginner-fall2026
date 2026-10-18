"""Color Python code the way VS Code does, when the pages are built.

highlight(text) returns the text escaped for HTML, with each token in a span. The
span's class names the color VS Code gives that token with its default theme and
the Python extension, which colors each name by what it is:

    hk  if, for, while, return, import, from, as, else, try, except, ...  purple
    hs  def, class, True, False, None, and, or, not, in, is, self, the
        f before an f-string, and the braces around a value in one         blue
    hf  functions and methods, where they are defined and called           brown
    hc  classes, types, and modules (pygame, Counter, int, range)          teal
    hv  variables, parameters, and attributes                              dark blue
    hn  constants, names in capitals (MESSAGE, pygame.QUIT)                mid blue
    hq  strings                                                            dark red
    he  escapes inside strings, such as \\n                                 red
    hd  numbers                                                            dark green
    hm  comments                                                           green

Anything else (operators, brackets, commas) keeps the block's plain color. The
colors themselves are in render.py's CSS: the hues of VS Code's light theme on a white
background, each darkened to at least 7:1 contrast so the code reads when it is
projected in a lit room, and the same in print. render.py checks the ratios when it
runs.

Copied from the Advanced Python course's build/hl.py, with MODULES trimmed to the
modules this course imports.
"""

import html
import re

CONTROL = {
    "if", "elif", "else", "for", "while", "return", "break", "continue", "pass",
    "import", "from", "as", "try", "except", "finally", "raise", "with", "yield",
    "assert", "del", "await", "async",
}
BLUE = {
    "def", "class", "lambda", "True", "False", "None", "and", "or", "not", "in", "is",
    "global", "nonlocal", "self", "cls",
}
BUILTIN_FUNCS = {
    "print", "len", "ord", "chr", "sum", "min", "max", "sorted", "abs", "round",
    "input", "open", "isinstance", "any", "all", "hash", "id", "repr", "format",
    "divmod", "pow", "iter", "next", "hex", "bin", "oct", "callable", "getattr",
    "setattr", "hasattr", "vars", "dir",
}
BUILTIN_CLASSES = {
    "int", "str", "float", "list", "dict", "set", "tuple", "bool", "range",
    "enumerate", "zip", "reversed", "map", "filter", "object", "type", "frozenset",
    "bytes", "super", "property", "staticmethod", "classmethod", "slice", "complex",
    "defaultdict",
}
# Modules the course imports. A name here is colored as a module when it is used
# like one (followed by a dot, or in an import line) and the code never assigns it.
# The beginner course imports pygame, random, and math; time is kept for the frame
# timer pages, which name it in prose.
MODULES = {"pygame", "random", "math", "time"}
SUBMODULES = {
    "display", "time", "event", "draw", "font", "mouse", "key", "image", "mixer",
    "transform", "path",
}

_TOKEN = re.compile(
    r"""
    (?P<comment>\#[^\n]*)
    |(?P<string>(?:[rR][bBfF]?|[bBfF][rR]?|[uU])?(?:\"\"\"|'''|"|'))
    |(?P<number>0[xX][0-9a-fA-F_]+|0[bB][01_]+|0[oO][0-7_]+
       |(?:\d[\d_]*(?:\.\d*)?|\.\d[\d_]*)(?:[eE][+-]?\d+)?[jJ]?)
    |(?P<name>[A-Za-z_]\w*)
    |(?P<space>[ \t]+|\n)
    |(?P<decorator>@(?=[A-Za-z_]))
    |(?P<op>.)
    """,
    re.X | re.S,
)
_ESCAPE = re.compile(r"\\(?:x[0-9a-fA-F]{2}|u[0-9a-fA-F]{4}|N\{[^}]*\}|[0-7]{1,3}|.|\n)", re.S)


def _span(cls, text):
    """Return text escaped, in a span of class cls (or bare if cls is empty)."""
    t = html.escape(text, quote=False)
    return f'<span class="{cls}">{t}</span>' if cls and text else t


def _names(context):
    """Return the names the code defines, imports, and assigns."""
    defs = set(re.findall(r"\bdef\s+([A-Za-z_]\w*)", context))
    classes = set(re.findall(r"\bclass\s+([A-Za-z_]\w*)", context))
    imported = set(re.findall(r"^\s*import\s+([A-Za-z_]\w*)", context, re.M))
    imported |= set(re.findall(r"^\s*from\s+([A-Za-z_]\w*)", context, re.M))
    assigned = set(re.findall(r"^\s*([A-Za-z_]\w*)\s*=(?!=)", context, re.M))
    assigned |= set(re.findall(r"\bfor\s+([A-Za-z_]\w*)\s+in\b", context))
    assigned |= set(re.findall(r"\bas\s+([A-Za-z_]\w*)\s*:", context))
    return defs, classes, imported, assigned


def _string_end(text, i, quote, raw):
    """Return the index just past the string that starts at i (after its quote)."""
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "\\" and not raw:
            i += 2
            continue
        if text.startswith(quote, i):
            return i + len(quote)
        if ch == "\n" and len(quote) == 1:
            return i
        i += 1
    return n


def _field_end(body, i):
    """Return the index of the } that closes the f-string field opened before i."""
    depth = 0
    n = len(body)
    while i < n:
        ch = body[i]
        if ch in "([{":
            depth += 1
        elif ch in ")]":
            depth -= 1
        elif ch == "}":
            if depth == 0:
                return i
            depth -= 1
        elif ch in "\"'":
            j = body.find(ch, i + 1)
            if j < 0:
                return -1
            i = j
        i += 1
    return -1


def _split_field(field):
    """Split an f-string field into its expression and its !conversion:spec tail."""
    depth = 0
    i = 0
    while i < len(field):
        ch = field[i]
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif ch in "\"'":
            j = field.find(ch, i + 1)
            i = j if j > 0 else len(field)
        elif depth == 0 and ch == "!" and field[i + 1:i + 2] != "=":
            return field[:i], field[i:]
        elif depth == 0 and ch == ":":
            return field[:i], field[i:]
        i += 1
    return field, ""


def _string(text, prefix, quote, ctx):
    """Return one whole string literal, prefix and quotes included, as HTML."""
    raw = "r" in prefix.lower()
    fmt = "f" in prefix.lower()
    close = len(text) >= len(prefix) + 2 * len(quote) and text.endswith(quote)
    body = text[len(prefix) + len(quote):len(text) - len(quote) if close else len(text)]
    out = _span("hs", prefix)
    piece = quote
    i = 0
    while i < len(body):
        ch = body[i]
        if fmt and body.startswith(("{{", "}}"), i):
            out += _span("hq", piece) + _span("he", body[i:i + 2])
            piece = ""
            i += 2
            continue
        if fmt and ch == "{":
            end = _field_end(body, i + 1)
            if end > 0:
                expr, tail = _split_field(body[i + 1:end])
                out += (
                    _span("hq", piece) + _span("hs", "{") + _code(expr, ctx)
                    + _span("hs", tail) + _span("hs", "}")
                )
                piece = ""
                i = end + 1
                continue
        m = _ESCAPE.match(body, i) if ch == "\\" and not raw else None
        if m:
            out += _span("hq", piece) + _span("he", m.group())
            piece = ""
            i = m.end()
            continue
        piece += ch
        i += 1
    return out + _span("hq", piece + (quote if close else ""))


def _code(text, ctx):
    """Return text as HTML with every token colored, using ctx for what names mean."""
    defs, classes, imported, assigned = ctx
    modules = (MODULES | imported) - assigned
    toks = []
    i = 0
    while i < len(text):
        m = _TOKEN.match(text, i)
        kind = m.lastgroup
        if kind == "string":
            opener = m.group()
            prefix = opener.rstrip("\"'")
            quote = opener[len(prefix):]
            end = _string_end(text, m.end(), quote, "r" in prefix.lower())
            toks.append(("string", text[i:end], (prefix, quote)))
            i = end
        else:
            toks.append((kind, m.group(), None))
            i = m.end()

    out = ""
    state = ""  # "import", "from", or "from-names" while inside an import line
    sig = []  # the tokens so far that are not spaces; a new line counts
    for k, (kind, tok, extra) in enumerate(toks):
        if kind == "space":
            if tok == "\n":
                state = ""
                sig.append(tok)
            out += tok
            continue
        prev = sig[-1] if sig else "\n"
        prev2 = sig[-2] if len(sig) > 1 else "\n"
        sig.append(tok if kind != "decorator" else "@")
        if kind == "string":
            out += _string(tok, extra[0], extra[1], ctx)
            continue
        if kind == "comment":
            out += _span("hm", tok)
            continue
        if kind == "number":
            out += _span("hd", tok)
            continue
        if kind == "decorator":
            out += _span("hf", tok)
            continue
        if kind != "name":
            out += html.escape(tok, quote=False)
            continue

        nxt = next((t[1] for t in toks[k + 1:] if t[0] != "space" or t[1] == "\n"), "")
        call = nxt == "("
        caps = re.fullmatch(r"[A-Z][A-Z0-9_]*", tok) is not None
        camel = tok[0].isupper() and not caps

        if tok in ("import", "from") and prev == "\n":
            state = tok
        elif tok == "import" and state == "from":
            state = "from-names"

        if tok in CONTROL:
            cls = "hk"
        elif tok in BLUE:
            cls = "hs"
        elif prev in ("def", "@"):
            cls = "hf"
        elif prev == "class":
            cls = "hc"
        elif state in ("import", "from"):
            cls = "hc"
        elif state == "from-names":
            cls = "hn" if caps else "hc" if (camel or tok in BUILTIN_CLASSES) else "hf"
        elif prev == ".":
            if call:
                cls = "hc" if camel else "hf"
            elif prev2 in modules and tok in SUBMODULES:
                cls = "hc"
            else:
                cls = "hn" if caps else "hc" if camel else "hv"
        elif call:
            cls = "hc" if (tok in BUILTIN_CLASSES or camel or tok in classes) else "hf"
        elif tok in modules and nxt == ".":
            cls = "hc"
        elif tok in BUILTIN_CLASSES or camel or tok in classes:
            cls = "hc"
        elif (tok in BUILTIN_FUNCS or tok in defs) and tok not in assigned:
            cls = "hf"
        elif caps:
            cls = "hn"
        else:
            cls = "hv"
        out += _span(cls, tok)
    return out


def highlight(text, context=None):
    """Return text as HTML with each token colored the way VS Code colors it.

    context is the whole program text when text is only part of it, so a name is
    colored by what it is in the whole program.
    """
    html_out = _code(text, _names(context if context is not None else text))
    plain = html.unescape(re.sub(r"<[^>]+>", "", html_out))
    assert plain == text, f"highlighting changed the code:\n{text}"
    return html_out
