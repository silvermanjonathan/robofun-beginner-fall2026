"""Session 8 worksheet: trace hangman before you run it.

Covers tools 1 and 2 of the session 8 build: the show function and the game loop. The
programs come straight from the session 8 entry in sessions_b.py, so the sheet and the
page cannot differ. Every row is worked out here with the program's own tests, using
the show function from the page itself, and then checked against a real run of the
program made with render.run_snippet when the site is built. The build stops if a run
disagrees with a row, or if a sentence in an answer stops being true.
"""

import render
from worksheet import KEY, brief_section, code, head, lines, sheet, trace_table

SLUG = "session08_worksheet"
S8 = [s for s in render.SESSIONS if s["num"] == 8][0]
TOOL1, TOOL2 = S8["brief"]["tools"][0], S8["brief"]["tools"][1]
assert [TOOL1["title"], TOOL2["title"]] == [
    "Tool 1: show, one line at a time", "Tool 2: the game, one line at a time",
], "session 8's tools moved; point the worksheet at the right ones"

SECRET, GUESSED = "SPYGLASS", "SAG"
assert TOOL1["code"].endswith(f'print(show("{SECRET}", "{GUESSED}"))')
assert TOOL2["code"].startswith(f'secret = "{SECRET}"\n')
FUNC = TOOL2["prefix"].rstrip("\n")
assert TOOL1["code"].startswith(FUNC), "tool 2 no longer starts from tool 1's function"
TYPED = TOOL2["stdin"].split()
MAX_MISSES = 6
assert f"while misses < {MAX_MISSES} and show(secret, guessed) != secret:" in TOOL2["code"]

# the page's own show function, so each row's last column is what that function returns
_NS = {}
exec(FUNC, _NS)
show = _NS["show"]

PASS_DONE = (1, 4, 6)
TURN_DONE = (1, 3, 6)
FILE = "Jonathan_session08.py"


def quoted(text):
    """A string the way the program writes it, so an empty string can be seen."""
    return '"' + text + '"'


def pass_rows():
    """One row for each pass of show's for loop, on the page's own test call."""
    rows, shown = {}, ""
    for n, ch in enumerate(SECRET, start=1):
        hit = ch in GUESSED
        shown = shown + (ch if hit else "_")
        rows[n] = [n, ch, hit, quoted(shown)]
    out, rc = render.run_snippet(TOOL1["code"], fname=FILE)
    assert rc == 0 and out == shown == show(SECRET, GUESSED), out
    return rows


def turn_rows():
    """One row for each turn of the game loop, with the page's own typed letters."""
    rows, guessed, misses = {}, "", 0
    feed = iter(TYPED)
    said = []
    turn = 0
    while misses < MAX_MISSES and show(SECRET, guessed) != SECRET:
        turn += 1
        guess = next(feed).strip().upper()
        if guess in guessed:
            branch, line = "if", "You already tried that one."
        elif guess in SECRET:
            guessed = guessed + guess
            branch, line = "elif", "Yes."
        else:
            guessed = guessed + guess
            misses = misses + 1
            branch, line = "else", "No."
        said.append(line)
        rows[turn] = [turn, guess, branch, quoted(guessed), misses, show(SECRET, guessed)]
    assert next(feed, None) is None, "the page types more letters than the game reads"

    # the real run: four lines a turn (the word, the misses, the prompt, the reply), then one
    out, rc = render.run_snippet(TOOL2["code"], preamble=TOOL2["prefix"],
                                 stdin=TOOL2["stdin"], fname=FILE)
    got = out.splitlines()
    assert rc == 0 and len(got) == 4 * turn + 1, out
    before = [show(SECRET, ""), 0]
    for n in range(1, turn + 1):
        word, count, prompt, reply = got[4 * (n - 1):4 * n]
        assert word == before[0] and count == f"misses: {before[1]} of {MAX_MISSES}", (n, word, count)
        assert prompt.strip().upper().endswith(rows[n][1]) and reply == said[n - 1], (n, prompt, reply)
        before = [rows[n][5], rows[n][4]]
    assert got[-1] == f"You got it: {SECRET}", got[-1]
    return rows


def facts():
    """Compute everything the sheet's sentences depend on."""
    passes, turns = pass_rows(), turn_rows()

    s_passes = [n for n, r in passes.items() if r[1] == "S"]
    assert s_passes == [1, 7, 8] and all(passes[n][2] for n in s_passes)
    assert GUESSED.count("S") == 1 and passes[8][3].count("S") == 3
    assert not set(PASS_DONE) & {7, 8}, "passes 7 and 8 are the question; keep them blank"

    miss_turns = [n for n, r in turns.items() if r[2] == "else"]
    same_turns = [n for n, r in turns.items() if r[2] == "if"]
    assert miss_turns == [4] and same_turns == [5], (miss_turns, same_turns)
    assert not set(TURN_DONE) & {4, 5}, "turns 4 and 5 are the question; keep them blank"
    last = max(turns)
    assert last == 8 and turns[last][5] == SECRET and turns[last][4] == 1
    return {"passes": passes, "turns": turns, "last": last}


_FACTS = {}


def get_facts():
    """Compute the facts once per build; the sheet and the key share them."""
    if not _FACTS:
        _FACTS.update(facts())
    return _FACTS


def done_rows(rows, worked):
    """Return the rows shown filled in: the worked ones on the sheet, every one in the key."""
    return {n: v for n, v in rows.items() if KEY["on"] or n in worked}


def tool1(f):
    b = '<div class="t1"><h3>' + TOOL1["title"].split(",")[0] + '</h3>'
    b += ("<p>The last line calls <code>show</code> with the secret word "
          f"<code>\"{SECRET}\"</code> and the guessed letters <code>\"{GUESSED}\"</code>.</p>")
    b += ("<p>Each row is one pass of the <code>for</code> loop. <code>ch</code> is the letter "
          "for that pass. Write True or False for the test on line 4. Then write the string "
          "that <code>shown</code> holds when the pass ends. Shaded rows are done for you.</p>")
    b += '<div class="two-up">' + code(TOOL1["code"])
    b += trace_table(
        ["pass", "ch", "ch in guessed?", "shown"],
        ["start", "", "", quoted("")],
        list(f["passes"]),
        {"ch": lambda n: f["passes"][n][1]},
        q_cols=("ch in guessed?",),
        done=done_rows(f["passes"], PASS_DONE),
        index="pass",
        widths=[19, 12, 29, 40],
    ) + "</div>"
    b += ('<div class="keep"><p>On passes 7 and 8, <code>ch</code> is S. Is '
          "<code>ch in guessed</code> True or False on those two passes? How many times is S "
          "in the string that <code>show</code> returns?</p>"
          + lines(2, "True on both passes. S is in the returned string 3 times, from passes "
                  "1, 7, and 8. The player guessed S once, but the test on line 4 runs once "
                  "for each letter of <code>secret</code>.")
          + "</div></div>")
    return b


def tool2(f):
    turns = f["turns"]
    b = '<div class="t2"><h3>' + TOOL2["title"].split(",")[0] + '</h3>'
    b += ("<p>This is the game from tool 2. The <code>show</code> function from tool 1 is "
          "above it in your file. The player types "
          + ", ".join(TYPED[:-1]) + ", and " + TYPED[-1] + ".</p>")
    b += code(TOOL2["code"])
    b += ('<div class="t2table"><p>Each row is one turn of the <code>while</code> loop. '
          "<code>guess</code> is the "
          "letter after line 8, so it is a capital. The gate on lines 9 to 17 has three "
          "branches. In the third column, write which branch runs: if, elif, or else. Then "
          "write what <code>guessed</code> and <code>misses</code> hold when the turn ends, "
          "and the string that <code>show(secret, guessed)</code> returns then. Shaded rows "
          "are done for you.</p>")
    b += trace_table(
        ["turn", "guess", "branch that runs", "guessed", "misses", "show(secret, guessed)"],
        ["start", "", "", quoted(""), 0, show(SECRET, "")],
        list(turns),
        {"guess": lambda n: turns[n][1]},
        q_cols=("branch that runs",),
        done=done_rows(turns, TURN_DONE),
        index="turn",
        widths=[10, 11, 19, 20, 12, 28],
    )
    b += ('<div class="keep"><p>Which turn adds 1 to <code>misses</code>? Which turn leaves '
          "<code>guessed</code> and <code>misses</code> the same, and which branch runs on "
          "that turn?</p>"
          + lines(3, "Turn 4 adds 1 to <code>misses</code>: Z is not in <code>secret</code>, "
                  "so the else branch runs. Turn 5 leaves both the same: S is already in "
                  "<code>guessed</code>, so the if branch runs, and Python skips the elif and "
                  "the else.")
          + "</div>")
    b += (f'<div class="keep"><p>After turn {f["last"]}, Python checks the condition on line 4 '
          "again and the loop stops. Which side of <code>and</code> is False, and why?</p>"
          + lines(3, "The right side. <code>show(secret, guessed)</code> returns "
                  f"{SECRET}, which is the same as <code>secret</code>, so <code>!=</code> "
                  f"gives False. The left side, <code>misses &lt; {MAX_MISSES}</code>, is "
                  f"still True, because <code>misses</code> is {turns[f['last']][4]}.")
          + "</div></div></div>")
    return b


TITLE = "trace hangman before you run it"
COVERS = S8["worksheet"]["covers"]
# Page breaks for the printed sheet; checked against the PDF (see README). Tool 1 is one
# page. Tool 2's program is page 2 and its table is page 3, which face each other in a
# packet printed double-sided and stapled on the left.
PRINT_CSS = ".t2,.t2table{break-before:page}"
# Tool 1's program is short, so on paper and on a wide screen it sits beside its table.
SIDE_BY_SIDE = ".t1 .two-up{grid-template-columns:minmax(0,46fr) minmax(0,54fr); align-items:start}"
HEAD = (head(PRINT_CSS) + "<style>\n@media (min-width:1000px){" + SIDE_BY_SIDE + "}\n"
        "@media print{" + SIDE_BY_SIDE + "}\n</style>\n")


def worksheet08():
    """Return the session 8 worksheet body."""
    f = get_facts()
    title = ("Answer key: " if KEY["on"] else "Worksheet: ") + TITLE
    return sheet(S8, title, COVERS, SLUG, [brief_section(S8, tool1(f) + tool2(f))])


def worksheet08_key():
    """Return the teacher's answer key: the worksheet with every slot filled."""
    KEY["on"] = True
    try:
        return worksheet08()
    finally:
        KEY["on"] = False
