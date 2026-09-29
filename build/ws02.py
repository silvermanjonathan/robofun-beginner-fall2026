"""Session 2 worksheet: work out True or False before you run it.

Covers chunks 4 to 6 of session 2: and, or, and the while loop's stopping condition.
The programs come straight from
the session 2 entry in sessions_a.py, so the sheet and the page cannot differ. Every
True or False in a worked or key row is Python's own comparison, and every printed line
in the key comes from running the program with render.run_snippet when the site is built.
The build stops if a run disagrees with a row, or if a sentence's numbers stop being true.
"""

import render
from worksheet import (KEY, chunk_section, code, head, lines, run_table,
                       sheet, trace_table)

SLUG = "session02_worksheet"
S2 = [s for s in render.SESSIONS if s["num"] == 2][0]
CH4, CH5, CH6 = (S2["chunks"][n]["code"] for n in (3, 4, 5))
assert [S2["chunks"][n]["title"] for n in (3, 4, 5)] == [
    "and: both must be True", "or: one is enough", "A while loop and its stopping condition",
], "session 2's chunks moved; point the worksheet at the right ones"

CH6_OR = CH6.replace(' and answer != "no"', ' or answer != "no"')
assert CH6_OR.split("\n")[1].startswith("while ")
assert CH6_OR.count(" or answer") == 1 and CH6_OR.count(" and ") == CH6.count(" and ") - 1

# Every rider and visitor is a pair of values for lines 1 and 2 of the program.
RIDERS = [(52, True), (52, False), (48, False), (48, True),
          (40, True), (60, False), (49, False), (49, True)]
VISITORS = [(False, True), (True, False), (True, True), (False, False)]
TYPED_AND = ["maybe", "soon", "yes"]   # the chunk 6 run on the session page
TYPED_OR = ["maybe", "yes", "no"]

RIDER_DONE = (1, 4, 7)
VISITOR_DONE = (1,)
CHECK_DONE = (1,)


def run(src, stdin=None):
    """Run a program the way the session pages do; return its output lines."""
    out, rc = render.run_snippet(src, stdin=stdin, fname="Jonathan_session02.py")
    return out, rc


def with_values(src, **values):
    """Return src with each named assignment line set to a new value, one line each."""
    lines_ = src.split("\n")
    for name, value in values.items():
        hits = [k for k, ln in enumerate(lines_) if ln.startswith(name + " = ")]
        assert len(hits) == 1, name
        lines_[hits[0]] = f"{name} = {value!r}"
    return "\n".join(lines_)


def printed(src):
    """Return the one line a gate program prints."""
    out, rc = run(src)
    assert rc == 0 and "\n" not in out, out
    return out


def rider_rows():
    """Every row of the rider table: the comparisons, and the line a real run prints."""
    rows = {}
    for n, (height, has_ticket) in enumerate(RIDERS, start=1):
        tall = height > 48
        both = height > 48 and has_ticket
        line = printed(with_values(CH4, height=height, has_ticket=has_ticket))
        assert (line == "Board the coaster.") == both, (n, line)
        rows[n] = [n, height, has_ticket, tall, both, line]
    return rows


def visitor_rows(src=CH5):
    """Every row of the visitor table: the whole condition, and the line a real run prints."""
    rows = {}
    for n, (is_staff, has_pass) in enumerate(VISITORS, start=1):
        either = is_staff or has_pass
        line = printed(with_values(src, is_staff=is_staff, has_pass=has_pass))
        if src == CH5:
            assert (line == "Gate opens.") == either, (n, line)
        rows[n] = [n, is_staff, has_pass, either, line]
    return rows


def check_rows(join, typed):
    """Every check of the chunk 6 condition, run the way the loop runs it."""
    rows = {}
    answer = ""
    feed = iter(typed)
    check = 0
    while True:
        check += 1
        left = answer != "yes"
        right = answer != "no"
        whole = (left and right) if join == "and" else (left or right)
        rows[check] = [check, f'"{answer}"', left, right, whole]
        if not whole:
            break
        answer = next(feed, None)
        if answer is None:
            break
    return rows


def loop_run(src, typed):
    """Run a chunk 6 program with answers piped in; return its output lines."""
    out, rc = run(src, stdin="".join(t + "\n" for t in typed))
    return out.splitlines(), rc


def facts():
    """Compute everything the sheet's sentences depend on, and check it against real runs."""
    riders = rider_rows()
    visitors = visitor_rows()
    swapped = visitor_rows(CH5.replace("is_staff or has_pass", "is_staff and has_pass"))
    and_checks = check_rows("and", TYPED_AND)
    or_checks = check_rows("or", TYPED_OR)

    and_out, rc = loop_run(CH6, TYPED_AND)
    assert rc == 0 and len(and_out) == len(TYPED_AND) + 1, and_out
    asked = sum(1 for r in and_checks.values() if r[4])
    assert asked == sum(1 for ln in and_out if ln.startswith("Ready?")) == 3
    assert list(and_checks) == [1, 2, 3, 4] and not and_checks[4][4] and not and_checks[4][2]

    or_out, rc = loop_run(CH6_OR, TYPED_OR)
    # every typed answer is taken and the loop asks once more: the fourth input() finds
    # nothing left to read, which is what the never-ending loop looks like with piped input
    assert rc != 0 and "EOFError" in or_out[-1], or_out
    assert sum(1 for ln in or_out if ln.startswith("Ready?")) == len(TYPED_OR)
    assert all(r[4] for r in or_checks.values()) and len(or_checks) == 4
    assert or_checks[3][2] is False and or_checks[3][3] is True
    assert or_checks[4][2] is True and or_checks[4][3] is False

    boarders = [n for n, r in riders.items() if r[4]]
    shut = [n for n, r in visitors.items() if r[4] == "Gate stays shut."]
    changed = [n for n in visitors if visitors[n][4] != swapped[n][4]]
    assert boarders == [1, 8], boarders
    assert shut == [4], shut
    assert changed == [1, 2], changed
    assert swapped[3][4] == "Gate opens." and swapped[4][4] == "Gate stays shut."
    assert not set(RIDER_DONE) & {2}, "rider 2 is the run question; keep it blank"

    return {
        "riders": riders, "visitors": visitors, "and_checks": and_checks,
        "or_checks": or_checks, "and_out": and_out,
        "run4": [("rider 2", printed(with_values(CH4, has_ticket=False))),
                 ("rider 8", printed(with_values(CH4, height=49)))],
        "run5": [("visitor 4", printed(with_values(CH5, has_pass=False)))],
    }


_FACTS = {}


def get_facts():
    """Compute the facts once per build; the sheet and the key share them."""
    if not _FACTS:
        _FACTS.update(facts())
    return _FACTS


def done_rows(rows, worked):
    """Return the rows shown filled in: the worked ones on the sheet, every one in the key."""
    return {n: v for n, v in rows.items() if KEY["on"] or n in worked}


def chunk4(f):
    b = "<p><code>and</code> is True only when both sides are True.</p>"
    b += '<div class="two-up">' + code(CH4, "chunk 4")
    b += "<p>Each row is one rider. Fill in the blanks. Shaded rows are done for you.</p>"
    b += trace_table(
        ["rider", "height", "has_ticket", "height > 48?", "height > 48 and has_ticket?",
         "what it prints"],
        None,
        range(1, len(RIDERS) + 1),
        {"height": lambda n: RIDERS[n - 1][0], "has_ticket": lambda n: RIDERS[n - 1][1]},
        q_cols=("height > 48?", "height > 48 and has_ticket?"),
        done=done_rows(f["riders"], RIDER_DONE),
        index="rider",
        widths=[8, 11, 14, 14, 21, 32],
    ) + "</div>"
    b += ('<div class="keep"><p>Which riders board the coaster? Why?</p>'
          + lines(2, "Riders 1 and 8. Theirs are the only rows where both sides are True.")
          + "</div>")
    b += ('<div class="keep"><h3>Run it</h3>'
          "<p>Put rider 2's values in lines 1 and 2, then run. Do the same for rider 8. "
          "Do not erase a wrong prediction.</p>"
          + run_table(f["run4"], label="Run") + "</div>")
    return chunk_section(S2, 4, b)


def chunk5(f):
    b = "<p><code>or</code> is True when either side is True.</p>"
    b += '<div class="two-up">' + code(CH5, "chunk 5")
    b += "<p>Each row is one visitor. Fill in the blanks. The shaded row is done for you.</p>"
    b += trace_table(
        ["visitor", "is_staff", "has_pass", "is_staff or has_pass?", "what it prints"],
        None,
        range(1, len(VISITORS) + 1),
        {"is_staff": lambda n: VISITORS[n - 1][0], "has_pass": lambda n: VISITORS[n - 1][1]},
        q_cols=("is_staff or has_pass?",),
        done=done_rows(f["visitors"], VISITOR_DONE),
        index="visitor",
        widths=[11, 16, 16, 27, 30],
    ) + "</div>"
    b += ('<div class="keep"><p>Which visitor is kept out? Why?</p>'
          + lines(2, "Visitor 4. Both sides are False, and <code>or</code> needs at least one "
                  "True side.")
          + "</div>")
    b += ('<div class="keep"><h3>Run it</h3>'
          "<p>Put visitor 4's values in lines 1 and 2, then run. Do not erase a wrong "
          "prediction.</p>"
          + run_table(f["run5"], label="Run") + "</div>")
    b += ('<div class="keep"><h3>If you have time</h3>'
          "<p>Change <code>or</code> to <code>and</code> on line 3. Which visitors now get a "
          "different line?</p>"
          + lines(2, "Visitors 1 and 2. Each has one True side: enough for <code>or</code>, not "
                  "for <code>and</code>. They now get Gate stays shut.")
          + "</div>")
    return chunk_section(S2, 5, b)


LOOP_HEADERS_AND = ["check", "answer", 'answer != "yes"?', 'answer != "no"?',
                    'answer != "yes" and answer != "no"?']
LOOP_WIDTHS = [8, 14, 18, 18, 42]
LOOP_HEADERS_OR = ["check", "answer", 'answer != "yes"?', 'answer != "no"?',
                   'answer != "yes" or answer != "no"?']


def chunk6(f):
    b = "<p><code>!=</code> means is not equal to. <code>\"\"</code> is empty text.</p>"
    b += '<div class="two-up">' + code(CH6, "chunk 6")
    b += ("<p>Someone types maybe, then soon, then yes. Each row is one check of the "
          "condition. Fill in the blanks. The shaded row is done for you.</p>")
    ac = f["and_checks"]
    b += trace_table(
        LOOP_HEADERS_AND, None, list(ac),
        {"answer": lambda n: ac[n][1]},
        q_cols=LOOP_HEADERS_AND[2:],
        done=done_rows(ac, CHECK_DONE),
        index="check",
        widths=LOOP_WIDTHS,
    ) + "</div>"
    b += ('<div class="keep"><p>How many times is the question asked? Which check stops the '
          "loop?</p>"
          + lines(2, "3 times. Check 4 stops it: <code>answer</code> is \"yes\", so "
                  "<code>answer != \"yes\"</code> is False, and <code>and</code> needs both "
                  "sides True.")
          + "</div>")
    b += ('<div class="keep"><h3>Run it</h3>'
          "<p>Predict each line, then run it and type maybe, soon, yes. Do not erase a wrong "
          "prediction.</p>"
          + run_table([("line " + str(k + 1), ln) for k, ln in enumerate(f["and_out"])])
          + "</div>")

    oc = f["or_checks"]
    b += "<h3>The same loop with or</h3>"
    b += '<div class="two-up">'
    b += ("<p>Line 2 now says <code>or</code>. Someone types maybe, then yes, then no. Trace "
          "it on paper only.</p>")
    b += code(CH6_OR.split("\n")[1], "chunk 6, line 2 with or")
    b += trace_table(
        LOOP_HEADERS_OR, None, list(oc),
        {"answer": lambda n: oc[n][1]},
        q_cols=LOOP_HEADERS_OR[2:],
        done=done_rows(oc, CHECK_DONE),
        index="check",
        widths=LOOP_WIDTHS,
    ) + "</div>"
    b += ('<div class="keep"><p>Does this loop ever stop? Why?</p>'
          + lines(2, "No. Every answer makes at least one side True: yes makes "
                  "<code>answer != \"no\"</code> True, and anything else makes "
                  "<code>answer != \"yes\"</code> True. <code>or</code> needs only one True "
                  "side. Run with maybe, yes, and no typed, it asks a fourth time.")
          + "</div>")
    return chunk_section(S2, 6, b)


TITLE = "work out True or False before you run it"
COVERS = S2["worksheet"]["covers"]
# Page breaks for the printed sheet; checked against the PDF (see README).
PRINT_CSS = "main section:nth-of-type(3){break-before:page}"
HEAD = head(PRINT_CSS)


def worksheet02():
    """Return the session 2 worksheet body."""
    f = get_facts()
    title = ("Answer key: " if KEY["on"] else "Worksheet: ") + TITLE
    return sheet(S2, title, COVERS, SLUG, [chunk4(f), chunk5(f), chunk6(f)])


def worksheet02_key():
    """Return the teacher's answer key: the worksheet with every slot filled."""
    KEY["on"] = True
    try:
        return worksheet02()
    finally:
        KEY["on"] = False
