"""Session 9 worksheet: trace tic tac toe before you run it.

Covers chunk 5 (the eight tests of the gate in winner) and chunk 9 (the finished game loop).
The programs come straight from session09.py, so the sheet and the page cannot
differ. Every row is worked out here with the page's own winner function and the
page's own typed moves, and then checked against a real run of the page's program
made with render.run_snippet when the site is built. The build stops if a run
disagrees with a row, or if a sentence in an answer stops being true.
"""

import re

import render
import session09 as src
from worksheet import KEY, chunk_section, code, head, lines, sheet, trace_table

SLUG = "session09_worksheet"
S9 = [s for s in render.SESSIONS if s["num"] == 9][0]
CH5, CH9 = S9["chunks"][4], S9["chunks"][8]
assert [CH5["title"], CH9["title"]] == ["Eight ways to win", "A letter instead of a number"], \
    "session 9's chunks moved; point the worksheet at the right ones"
assert CH5["code"] == src.C5 and CH9["code"] == src.C9
FILE = "Jonathan_session09.py"

# the page's own winner function, so every row's last column is what that function returns
_NS = {}
exec(src.WINNER, _NS)
winner = _NS["winner"]

# the eight tests of the gate, in the order winner makes them, read from the page's code
TEST_LINES = [m.group(0) for m in re.finditer(
    r"(?:if|elif) board\[\d\] == board\[(\d)\] and board\[\1\] == board\[\d\]:", src.WINNER)]
TESTS = [tuple(int(d) for d in re.findall(r"\d", line)[:2] + re.findall(r"\d", line)[-1:])
         for line in TEST_LINES]
assert len(TESTS) == 8 and src.WINNER.count(" board[") - src.WINNER.count("return board[") == 32, TESTS

TEST_DONE = (1, 3, 5)
PASS_DONE = (1, 4, 6)
NOT_MADE = "not made"


def quoted(text):
    """A string the way the program writes it, so an empty string can be seen."""
    return '"' + text + '"'


def board_line(board):
    """The board as the line of Python that would make it."""
    return "board = [" + ", ".join(quoted(v) for v in board) + "]"


def start_board(line):
    """Read the list of nine strings out of a `board = [...]` line of the page's code."""
    board = re.findall(r'"([^"]*)"', line)
    assert len(board) == 9 and board_line(board) == line, line
    return board


def test_rows():
    """One row for each test in winner's gate, on chunk 5's test board after the typed move."""
    board = start_board(src.ALL_TEST)
    move = CH5["stdin"].strip()
    board[int(move) - 1] = "X"

    rows, returned = {}, None
    for n, (a, b, c) in enumerate(TESTS, start=1):
        slots = TEST_LINES[n - 1]
        if returned is not None:
            rows[n] = [n, slots, NOT_MADE, NOT_MADE]
            continue
        same = board[a] == board[b] and board[b] == board[c]
        rows[n] = [n, slots, ", ".join(quoted(board[k]) for k in (a, b, c)), same]
        if same:
            returned = (n, board[a])
    assert returned is not None and returned[1] == winner(board), returned

    out, rc = render.run_snippet(CH5["code"], stdin=CH5["stdin"], fname=FILE)
    assert rc == 0 and out.splitlines()[-1] == f"winner: {returned[1]}", out
    return rows, board, returned


def pass_rows():
    """One row for each pass of the game loop, with chunk 9's own typed moves."""
    board = start_board(src.EMPTY)
    marks = ["X", "O"]
    turns = 0
    feed = iter(CH9["stdin"].split())
    rows, asked, replies = {}, [], []
    n = 0
    while turns < 9 and winner(board) == "":
        n += 1
        player = marks[turns % 2]
        move = next(feed)
        asked.append(f"Player {player}, pick a square: {move}")
        if move == "X" or move == "O":
            branch = "if"
            replies.append("Type the number of a square, not a mark.")
        elif move in board:
            spot = int(move) - 1
            board[spot] = player
            turns = turns + 1
            branch = "elif"
        else:
            branch = "else"
            replies.append("That is not a free square. Try again.")
        rows[n] = [n, move, player, branch, turns, quoted(winner(board))]
    assert next(feed, None) is None, "the page types more moves than the game reads"

    out, rc = render.run_snippet(CH9["code"], stdin=CH9["stdin"], fname=FILE)
    got = out.splitlines()
    assert rc == 0 and [g for g in got if g.startswith("Player ")] == asked, out
    assert [g for g in got if g.startswith(("Type the", "That is"))] == replies, out
    assert got[-1] == f"{winner(board)} wins!", got[-1]
    return rows, board, turns


def facts():
    """Compute everything the sheet's sentences depend on."""
    tests, test_board, returned = test_rows()
    passes, end_board, turns = pass_rows()

    assert returned == (7, "X") and TESTS[6] == (0, 4, 8) and TESTS[7] == (2, 4, 6)
    assert [n for n, r in tests.items() if r[3] is False] == [1, 2, 3, 4, 5, 6]
    assert not set(TEST_DONE) & {7, 8}, "tests 7 and 8 are the question; keep them blank"

    same = [n for n in passes if passes[n][4] == (passes[n - 1][4] if n > 1 else 0)]
    assert same == [2, 3] and passes[2][3] == "if" and passes[3][3] == "else"
    assert passes[2][1] == "X" and passes[3][1] == "5" and end_board[4] == "X"
    assert [passes[n][2] for n in (2, 3, 4)] == ["O", "O", "O"] and passes[1][4] == 1
    assert not set(PASS_DONE) & {2, 3}, "passes 2 and 3 are the question; keep them blank"
    last = max(passes)
    assert last == 7 and turns == 5 and winner(end_board) == "X"
    assert end_board[3:6] == ["X", "X", "X"] and TESTS[1] == (3, 4, 5)
    return {"tests": tests, "test_board": test_board, "passes": passes, "last": last,
            "turns": turns}


_FACTS = {}


def get_facts():
    """Compute the facts once per build; the sheet and the key share them."""
    if not _FACTS:
        _FACTS.update(facts())
    return _FACTS


def done_rows(rows, worked):
    """Return the rows shown filled in: the worked ones on the sheet, every one in the key."""
    return {n: v for n, v in rows.items() if KEY["on"] or n in worked}


def chunk5(f):
    tests = f["tests"]
    b = ("<p>On chunk 5's test board, "
         f"player X typed {CH5['stdin'].strip()}, so the board is now:</p>")
    b += code(board_line(f["test_board"]))
    b += ("<p>The table has the eight tests of the gate in <code>winner</code>, in the order "
          "Python makes them. In the program, each test has a <code>return</code> line "
          "under it. For each test, write the three strings it compares, then True or "
          "False for the whole test. When a test is True, <code>winner</code> returns. If "
          f"Python never makes a test, write {NOT_MADE} in its row. Shaded rows are done "
          "for you.</p>")
    b += '<div class="gate">' + trace_table(
        ["test", "line of the gate", "the three strings", "True or False?"],
        None,
        list(tests),
        {"line of the gate": lambda n: tests[n][1]},
        q_cols=("True or False?",),
        done=done_rows(tests, TEST_DONE),
        index="test",
        widths=[7, 55, 21, 17],
    ) + "</div>"
    b += ('<div class="keep"><p>Which test is True, and what does <code>winner</code> '
          "return? Which test does Python never make, and why?</p>"
          + lines(3, "Test 7 is True: slots 0, 4, and 8 all hold X, so <code>winner</code> "
                  "returns <code>\"X\"</code>. Python never makes test 8, slots 2, 4, and 6. "
                  "A function stops at its <code>return</code>, and Python skips every "
                  "branch after the first one whose test is True.")
          + "</div>")
    return chunk_section(S9, 5, b)


def chunk9(f):
    passes = f["passes"]
    typed = CH9["stdin"].split()
    b = ("<p>This is the finished game. The <code>show</code> and <code>winner</code> "
         "functions are above it in your file. The players type "
         + ", ".join(typed[:-1]) + ", and " + typed[-1] + ".</p>")
    b += code(src.GAME9)
    b += ('<div class="t2table"><p>Each row is one pass of the <code>while</code> loop. '
          "<code>move</code> is what was typed on that pass. Write the value of "
          "<code>player</code>, which <code>marks[turns % 2]</code> gives. The gate that "
          "starts <code>if move == \"X\" or move == \"O\":</code> has three branches. "
          "Write which branch runs: if, elif, or else. Then write what <code>turns</code> "
          "holds when the pass ends, and the string that <code>winner(board)</code> "
          "returns then. Shaded rows are done for you.</p>")
    b += trace_table(
        ["pass", "move", "player", "branch that runs", "turns", "winner(board)"],
        ["start", "", "", "", 0, quoted("")],
        list(passes),
        {"move": lambda n: passes[n][1]},
        q_cols=("branch that runs",),
        done=done_rows(passes, PASS_DONE),
        index="pass",
        widths=[12, 12, 14, 24, 14, 24],
    )
    b += ('<div class="keep"><p>On which two passes does <code>turns</code> stay the same? '
          "Which branch runs on each of those passes?</p>"
          + lines(2, "Pass 2 and pass 3. On pass 2 the move is the letter X, so the if "
                  "branch runs. On pass 3 the move is 5, and <code>\"5\"</code> is not in "
                  "<code>board</code> any more because that slot holds X, so the else "
                  "branch runs.")
          + "</div>")
    b += ('<div class="keep"><p>The same player is asked on passes 2, 3, and 4. Why does '
          "<code>marks[turns % 2]</code> give the same mark all three times?</p>"
          + lines(2, f"<code>turns</code> is {passes[1][4]} at the start of each of those "
                  "passes. <code>1 % 2</code> is 1, and <code>marks[1]</code> is "
                  "<code>\"O\"</code>, so player O is asked each time.")
          + "</div>")
    b += (f'<div class="keep"><p>After pass {f["last"]}, Python checks the condition on the '
          "<code>while</code> line again and the loop stops. Which side of <code>and</code> "
          "is False, and why?</p>"
          + lines(3, "The right side. <code>winner(board)</code> returns <code>\"X\"</code>, "
                  "because slots 3, 4, and 5 all hold X, so <code>== \"\"</code> gives "
                  "False. The left side, <code>turns &lt; 9</code>, is still True, because "
                  f"<code>turns</code> is {f['turns']}.")
          + "</div></div>")
    return '<div class="t2">' + chunk_section(S9, 9, b) + "</div>"


TITLE = "trace tic tac toe before you run it"
COVERS = S9["worksheet"]["covers"]
# Page breaks for the printed sheet; checked against the PDF (see README). Chunk 5 is
# one page. Chunk 9's program is page 2 and its table is page 3, which face each other
# in a packet printed double-sided and stapled on the left.
PRINT_CSS = ".t2,.t2table{break-before:page}"
# The lines of the gate are long, so they sit on the left of their cells and never wrap.
GATE_CSS = ".gate table.trace td:nth-child(2){text-align:left; white-space:nowrap; font-size:14px}"
HEAD = (head(PRINT_CSS) + "<style>\n" + GATE_CSS + "\n@media print{"
        ".gate table.trace td:nth-child(2){font-size:8.4pt} .gate table.trace td{height:28px; padding:1px 6px; line-height:1.25}}\n</style>\n")


def worksheet09():
    """Return the session 9 worksheet body."""
    f = get_facts()
    title = ("Answer key: " if KEY["on"] else "Worksheet: ") + TITLE
    return sheet(S9, title, COVERS, SLUG, [chunk5(f), chunk9(f)])


def worksheet09_key():
    """Return the teacher's answer key: the worksheet with every slot filled."""
    KEY["on"] = True
    try:
        return worksheet09()
    finally:
        KEY["on"] = False
