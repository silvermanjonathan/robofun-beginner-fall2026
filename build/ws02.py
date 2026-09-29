"""Session 2 worksheet: work out True or False before you run it.

Covers chunks 4 to 6 of session 2 (and, or, the while loop's stopping condition) and
the lines of the ride-operator build that use them. The programs come straight from
the session 2 entry in sessions_a.py, so the sheet and the page cannot differ. Every
True or False in a worked or key row is Python's own comparison, and every printed line
in the key comes from running the program with render.run_snippet when the site is built.
The build stops if a run disagrees with a row, or if a sentence's numbers stop being true.
"""

import render
from worksheet import (KEY, brief_section, chunk_section, code, head, lines, run_table,
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


# The ride operator, written out only so the key's three lines are checked in a real
# program. It is not printed anywhere.
BUILD_CHECK = '''height = input("Height in inches: ")
height = int(height)
ticket = ""
while ticket != "yes" and ticket != "no":
    ticket = input("Ticket? Type yes or no: ")
if height > 48 and ticket == "yes":
    print("OPEN")
elif height == 48:
    print("STAFF")
else:
    print("CLOSED")'''


def check_build():
    """Run the build's expected-and-got cases through the key's lines; fail loudly if one is off."""
    cases = [("52\nyes\n", "OPEN"), ("52\nno\n", "CLOSED"), ("48\nyes\n", "STAFF"),
             ("52\nmaybe\nyes\n", "OPEN")]
    for stdin, want in cases:
        out, rc = run(BUILD_CHECK, stdin=stdin)
        assert rc == 0 and out.splitlines()[-1] == want, (stdin, out)
    # asked twice when maybe comes first
    out, _ = run(BUILD_CHECK, stdin="52\nmaybe\nyes\n")
    assert out.count("Ticket?") == 2, out
    missing = BUILD_CHECK.replace('ticket = ""\n', "")
    out, rc = run(missing, stdin="52\nyes\n")
    assert rc != 0 and "NameError: name 'ticket' is not defined" in out, out


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

    check_build()
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
    b = ("<p><code>and</code> joins two conditions into one condition. The whole condition is "
         "True only when both sides are True. This is the chunk 4 program.</p>")
    b += '<div class="two-up">' + code(CH4, "chunk 4, as on the session 2 page")
    b += ("<p>Each row of the table is one rider, as if lines 1 and 2 held that rider's values. "
          "In the two columns whose headings end in a question mark, write True or False. In "
          "the last column, write the line the program prints for that rider. Three rows are "
          "done for you, shaded, so you can check your working against them as you go. The "
          "rows in between are yours.</p>")
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
    b += ('<div class="keep"><p>Look down your last column. Which riders board the coaster? '
          "Write their numbers, then one sentence: what do their rows have that no other row "
          "has?</p>"
          + lines(2, "Riders 1 and 8. Theirs are the only rows where <code>height &gt; 48</code> "
                  "is True and <code>has_ticket</code> is True. <code>and</code> gives True only "
                  "when both sides are True, so every other rider gets Step aside.")
          + "</div>")
    b += "<h3>Run it</h3>"
    b += ("<p>Start from the program as written each time, and change one line per run. For "
          "rider 2, change line 2 to <code>has_ticket = False</code>. For rider 8, change line 1 "
          "to <code>height = 49</code>. Copy what it printed next to your prediction, and mark "
          "it right or wrong. Do not erase a wrong prediction.</p>")
    b += run_table(f["run4"], label="Run")
    return chunk_section(S2, 4, b)


def chunk5(f):
    b = ("<p><code>or</code> joins two conditions too. The whole condition is True when "
         "either side is True. This is the chunk 5 program.</p>")
    b += '<div class="two-up">' + code(CH5, "chunk 5, as on the session 2 page")
    b += ("<p>Each row is one visitor at the gate, as if lines 1 and 2 held that visitor's "
          "values. In the column whose heading ends in a question mark, write True or False. "
          "In the last column, write the line the program prints for that visitor. Visitor 1 "
          "is the program as written, done for you, shaded. Visitors 2, 3, and 4 are yours.</p>")
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
    b += ('<div class="keep"><p>Which visitor does the gate keep out? Write the number, then '
          "one sentence: why does the gate stay shut for that visitor?</p>"
          + lines(2, "Visitor 4. <code>is_staff</code> and <code>has_pass</code> are both False. "
                  "<code>or</code> needs at least one True side, so the whole condition is False "
                  "and the <code>else</code> block runs: Gate stays shut.")
          + "</div>")
    b += "<h3>Run it</h3>"
    b += ("<p>Start from the program as written. For visitor 4, change line 2 to "
          "<code>has_pass = False</code> and run it. Do not erase a wrong prediction.</p>")
    b += run_table(f["run5"], label="Run")
    b += ('<div class="keep"><h3>If you have time: and in place of or</h3>'
          "<p>On paper, change <code>or</code> to <code>and</code> on line 3. Which visitors "
          "would now get a different line printed? Write their numbers, then one sentence "
          "saying why.</p>"
          + lines(2, "Visitors 1 and 2. Each has one True side and one False side. With "
                  "<code>or</code>, one True side opens the gate. With <code>and</code>, both "
                  "sides must be True, so visitors 1 and 2 would get Gate stays shut. Visitor 3 "
                  "still gets Gate opens and visitor 4 still gets Gate stays shut.")
          + "</div>")
    return chunk_section(S2, 5, b)


LOOP_HEADERS_AND = ["check", "answer", 'answer != "yes"?', 'answer != "no"?',
                    'answer != "yes" and answer != "no"?']
LOOP_WIDTHS = [8, 14, 18, 18, 42]
LOOP_HEADERS_OR = ["check", "answer", 'answer != "yes"?', 'answer != "no"?',
                   'answer != "yes" or answer != "no"?']


def chunk6(f):
    b = ("<p>A <code>while</code> loop checks its condition before every pass. When the "
         "condition is True, the block runs. The first time it is False, the loop stops "
         "and the line after the block runs.</p>"
         "<p><code>!=</code> means is not equal to. <code>\"\"</code> is empty text: two quote "
         "marks with nothing between them.</p>")
    b += '<div class="two-up">' + code(CH6, "chunk 6, as on the session 2 page")
    b += ("<p>Someone types maybe, then soon, then yes. Each row of the table is one check "
          "of the condition, in order. The answer column shows what <code>answer</code> holds "
          "at that check. In the three columns whose headings end in a question mark, write "
          "True or False. The last of them is the whole condition. Check 1 is done for you, "
          "shaded. Checks 2, 3, and 4 are yours.</p>")
    ac = f["and_checks"]
    b += trace_table(
        LOOP_HEADERS_AND, None, list(ac),
        {"answer": lambda n: ac[n][1]},
        q_cols=LOOP_HEADERS_AND[2:],
        done=done_rows(ac, CHECK_DONE),
        index="check",
        widths=LOOP_WIDTHS,
    ) + "</div>"
    b += ('<div class="keep"><p>At every check where the whole condition is True, the block '
          "runs and the question appears. How many times does the question appear? Which check "
          "stops the loop, and which side of the <code>and</code> is False there?</p>"
          + lines(2, "The question appears 3 times, at checks 1, 2, and 3. Check 4 stops the "
                  "loop. There <code>answer</code> is \"yes\", so <code>answer != \"yes\"</code> "
                  "is False. <code>and</code> needs both sides True, so the whole condition is "
                  "False, the loop stops, and the print line runs.")
          + "</div>")
    b += "<h3>Run it</h3>"
    b += ("<p>Before you run it, write the lines you expect to see in the terminal, including "
          "what is typed after each question. Then run it, type maybe, soon, and yes, "
          "and copy each line. Do not erase a wrong prediction.</p>")
    b += run_table([("line " + str(k + 1), ln) for k, ln in enumerate(f["and_out"])])

    oc = f["or_checks"]
    b += "<h3>The same loop with or</h3>"
    b += '<div class="two-up">'
    b += ("<p>Here is line 2 of the chunk 6 program with <code>or</code> in place of "
          "<code>and</code>. Every other line stays the same. Trace it on paper only. Someone "
          "types maybe, then yes, then no. Check 1 is done for you, shaded.</p>")
    b += code(CH6_OR.split("\n")[1], "chunk 6, line 2 with or")
    b += trace_table(
        LOOP_HEADERS_OR, None, list(oc),
        {"answer": lambda n: oc[n][1]},
        q_cols=LOOP_HEADERS_OR[2:],
        done=done_rows(oc, CHECK_DONE),
        index="check",
        widths=LOOP_WIDTHS,
    ) + "</div>"
    b += ('<div class="keep"><p>Does the loop stop at check 3 or at check 4? Is there any '
          "answer that would make the whole condition False? One sentence for each question.</p>"
          + lines(2, "No, the loop does not stop at check 3 or check 4. At check 3, "
                  "<code>answer != \"no\"</code> is True. At check 4, <code>answer != \"yes\"</code> "
                  "is True. With <code>or</code>, one True side is enough. No answer makes the "
                  "whole condition False: both sides would have to be False, so "
                  "<code>answer</code> would have to be yes and no at the same time. This loop "
                  "never stops. When it is run and maybe, yes, and no are typed, it asks the question "
                  "a fourth time.")
          + "</div>")
    return chunk_section(S2, 6, b)


def build():
    b = ("<p>The build asks for a height and a ticket answer. Write three of its lines here before you type them. Use <code>height</code> "
         "for the height, already changed to a whole number with <code>int()</code>, and "
         "<code>ticket</code> for the ticket answer.</p>")
    b += ('<div class="keep"><p>Step 2 keeps asking until the rider types yes or no. Write the '
          "<code>while</code> line. It is the chunk 6 loop with <code>ticket</code> in place of "
          "<code>answer</code>.</p>"
          + lines(1, "<code>while ticket != \"yes\" and ticket != \"no\":</code>")
          + "</div>")
    b += ('<div class="keep"><p>In chunk 6, the line <code>answer = \"\"</code> comes before the '
          "<code>while</code> line. Write the line that comes before your <code>while</code> "
          "line. Then one sentence: what happens if it is missing?</p>"
          + lines(2, "<code>ticket = \"\"</code>. Without it, Python checks the condition before "
                  "the first question is asked, <code>ticket</code> does not exist yet, and the "
                  "program crashes with a NameError.")
          + "</div>")
    b += ('<div class="keep"><p>Step 3 opens the ride only when the height clears 48 and the '
          "ticket answer is yes. Clears 48 means more than 48; exactly 48 goes to staff in step "
          "4. Write the <code>if</code> line.</p>"
          + lines(1, "<code>if height &gt; 48 and ticket == \"yes\":</code>")
          + "</div>")
    return brief_section(S2, b)


TITLE = "work out True or False before you run it"
COVERS = S2["worksheet"]["covers"]
# Page breaks for the printed sheet; checked against the PDF (see README).
PRINT_CSS = "main section:nth-of-type(3){break-before:page}"
HEAD = head(PRINT_CSS)


def worksheet02():
    """Return the session 2 worksheet body."""
    f = get_facts()
    title = ("Answer key: " if KEY["on"] else "Worksheet: ") + TITLE
    return sheet(S2, title, COVERS, SLUG, [chunk4(f), chunk5(f), chunk6(f), build()])


def worksheet02_key():
    """Return the teacher's answer key: the worksheet with every slot filled."""
    KEY["on"] = True
    try:
        return worksheet02()
    finally:
        KEY["on"] = False
