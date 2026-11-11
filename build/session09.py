# Session 9: tic tac toe in the terminal. Added November 2026 in the slot the cipher
# wheel had; the cipher wheel is now an extra page with no date (sessions_b.py).
# The whole session is one program, written one line at a time: a board stored as a
# list of nine strings, a function that prints it, a function that returns the winner,
# and a loop in which two players take turns.

# ---------------------------------------------------------------- the program, in parts

SHOW = '''def show(board):
    print(f" {board[0]} | {board[1]} | {board[2]}")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]}")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]}")'''

WINNER_ROWS = '''def winner(board):
    if board[0] == board[1] and board[1] == board[2]:
        return board[0]
    elif board[3] == board[4] and board[4] == board[5]:
        return board[3]
    elif board[6] == board[7] and board[7] == board[8]:
        return board[6]
    else:
        return ""'''

WINNER = '''def winner(board):
    if board[0] == board[1] and board[1] == board[2]:
        return board[0]
    elif board[3] == board[4] and board[4] == board[5]:
        return board[3]
    elif board[6] == board[7] and board[7] == board[8]:
        return board[6]
    elif board[0] == board[3] and board[3] == board[6]:
        return board[0]
    elif board[1] == board[4] and board[4] == board[7]:
        return board[1]
    elif board[2] == board[5] and board[5] == board[8]:
        return board[2]
    elif board[0] == board[4] and board[4] == board[8]:
        return board[0]
    elif board[2] == board[4] and board[4] == board[6]:
        return board[2]
    else:
        return ""'''

EMPTY = 'board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]'

ONE_MOVE = '''show(board)
move = input("Player X, pick a square: ")
spot = int(move) - 1
board[spot] = "X"
show(board)'''

C1 = EMPTY + '''
print(len(board))
print(board[4])
board[4] = "X"
print(board[4])
print(board)'''

C2_START = EMPTY + '\nboard[4] = "X"'
C2 = SHOW + "\n\n" + EMPTY + '\nboard[4] = "X"\nshow(board)'

C3 = SHOW + "\n\n" + EMPTY + "\n" + ONE_MOVE

ROW_TEST = 'board = ["X", "X", "3", "O", "O", "6", "7", "8", "9"]'
C4 = SHOW + "\n\n" + WINNER_ROWS + "\n\n" + ROW_TEST + "\n" + ONE_MOVE + '\nprint(f"winner: {winner(board)}")'

ALL_TEST = 'board = ["X", "O", "3", "4", "X", "O", "7", "8", "9"]'
C5 = SHOW + "\n\n" + WINNER + "\n\n" + ALL_TEST + "\n" + ONE_MOVE + '\nprint(f"winner: {winner(board)}")'

FUNCTIONS = SHOW + "\n\n" + WINNER + "\n\n"

GAME6 = EMPTY + '''
marks = ["X", "O"]
turns = 0
while turns < 9 and winner(board) == "":
    show(board)
    player = marks[turns % 2]
    move = input(f"Player {player}, pick a square: ")
    spot = int(move) - 1
    board[spot] = player
    turns = turns + 1

show(board)'''

VERDICT = '''
if winner(board) == "":
    print("Nobody wins. It is a draw.")
else:
    print(f"{winner(board)} wins!")'''

GAME7 = GAME6 + VERDICT

GAME8 = EMPTY + '''
marks = ["X", "O"]
turns = 0
while turns < 9 and winner(board) == "":
    show(board)
    player = marks[turns % 2]
    move = input(f"Player {player}, pick a square: ")
    if move in board:
        spot = int(move) - 1
        board[spot] = player
        turns = turns + 1
    else:
        print("That is not a free square. Try again.")

show(board)''' + VERDICT

GAME9 = EMPTY + '''
marks = ["X", "O"]
turns = 0
while turns < 9 and winner(board) == "":
    show(board)
    player = marks[turns % 2]
    move = input(f"Player {player}, pick a square: ")
    if move == "X" or move == "O":
        print("Type the number of a square, not a mark.")
    elif move in board:
        spot = int(move) - 1
        board[spot] = player
        turns = turns + 1
    else:
        print("That is not a free square. Try again.")

show(board)''' + VERDICT

C6, C7, C8, C9 = FUNCTIONS + GAME6, FUNCTIONS + GAME7, FUNCTIONS + GAME8, FUNCTIONS + GAME9

# The extension: the computer plays O. Shown without the two functions, which do not
# change; they are supplied as a run prefix with the import above them.
COMPUTER = EMPTY + '''
marks = ["X", "O"]
turns = 0
while turns < 9 and winner(board) == "":
    show(board)
    player = marks[turns % 2]
    if player == "X":
        move = input("Your move. Pick a square: ")
    else:
        move = random.choice(board)
        while move == "X" or move == "O":
            move = random.choice(board)
        print(f"The computer picks square {move}.")
    if move == "X" or move == "O":
        print("Type the number of a square, not a mark.")
    elif move in board:
        spot = int(move) - 1
        board[spot] = player
        turns = turns + 1
    else:
        print("That is not a free square. Try again.")

show(board)''' + VERDICT


# ------------------------------------------------------------------------- figures

INK = "#17181B"
SOFT = "#4A4D53"
TEAL = "#0E4D52"
CLAY = "#9C2B22"
OCHRE = "#8A5A00"
MONO = "font-family:JetBrains Mono,monospace"


def _grid(x, y, cell, width=4):
    """The four rules of a tic tac toe board whose top left corner is (x, y)."""
    out = []
    for k in (1, 2):
        out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%d"/>'
                   % (x + k * cell, y, x + k * cell, y + 3 * cell, INK, width))
        out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%d"/>'
                   % (x, y + k * cell, x + 3 * cell, y + k * cell, INK, width))
    return "".join(out)


def board_figure():
    """Each square with the number the player types and the index of its slot."""
    cell = 130
    x0, y0 = 30, 20
    out = ['<svg viewBox="0 0 450 470" role="img" style="max-width:450px;width:100%;height:auto;display:block;margin:14px 0" '
           'aria-label="The nine squares of the board. Square 1 is slot 0, square 2 is slot 1, '
           'and so on to square 9, which is slot 8. The slot is always one less than the square.">']
    out.append(_grid(x0, y0, cell))
    for i in range(9):
        cx = x0 + (i % 3) * cell + cell / 2
        cy = y0 + (i // 3) * cell
        out.append('<text x="%d" y="%d" text-anchor="middle" font-size="46" font-weight="700" fill="%s" style="%s">%d</text>'
                   % (cx, cy + 66, TEAL, MONO, i + 1))
        out.append('<text x="%d" y="%d" text-anchor="middle" font-size="20" fill="%s" style="%s">slot %d</text>'
                   % (cx, cy + 104, CLAY, MONO, i))
    out.append('<text x="30" y="436" font-size="18" fill="%s" style="%s">Big number: the square you type.</text>'
               % (SOFT, MONO))
    out.append('<text x="30" y="460" font-size="18" fill="%s" style="%s">Small number: the index of its slot.</text>'
               % (SOFT, MONO))
    out.append('</svg>')
    return "".join(out)


def lines_figure():
    """The eight ways to win, as three small boards: rows, columns, diagonals."""
    cell = 46
    groups = [("3 rows", [(0, 1, 2), (3, 4, 5), (6, 7, 8)]),
              ("3 columns", [(0, 3, 6), (1, 4, 7), (2, 5, 8)]),
              ("2 diagonals", [(0, 4, 8), (2, 4, 6)])]
    out = ['<svg viewBox="0 0 660 300" role="img" style="max-width:660px;width:100%;height:auto;display:block;margin:14px 0" '
           'aria-label="The eight ways to win, by slot. Rows: 0 1 2, 3 4 5, 6 7 8. Columns: 0 3 6, '
           '1 4 7, 2 5 8. Diagonals: 0 4 8 and 2 4 6.">']
    for g, (name, lines) in enumerate(groups):
        x0, y0 = 30 + g * 215, 44
        out.append('<text x="%d" y="26" font-size="20" font-weight="700" fill="%s" style="%s">%s</text>'
                   % (x0, TEAL, MONO, name))
        out.append(_grid(x0, y0, cell, 3))
        for i in range(9):
            out.append('<text x="%d" y="%d" text-anchor="middle" font-size="18" fill="%s" style="%s">%d</text>'
                       % (x0 + (i % 3) * cell + cell / 2, y0 + (i // 3) * cell + 29, INK, MONO, i))
        for a, b, c in lines:
            ax, ay = x0 + (a % 3) * cell + cell / 2, y0 + (a // 3) * cell + cell / 2
            cx, cy = x0 + (c % 3) * cell + cell / 2, y0 + (c // 3) * cell + cell / 2
            out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="8" '
                       'stroke-linecap="round" stroke-opacity="0.35"/>' % (ax, ay, cx, cy, CLAY))
        for k, (a, b, c) in enumerate(lines):
            out.append('<text x="%d" y="%d" font-size="19" fill="%s" style="%s">%d %d %d</text>'
                       % (x0, y0 + 3 * cell + 30 + k * 26, CLAY, MONO, a, b, c))
    out.append('</svg>')
    return "".join(out)


# ------------------------------------------------------------------------ the session

SESSION09 = {
 "num": 9,
 "slug": "session09_tic_tac_toe",
 "title": "Tic tac toe",
 "subtitle": "A two-player game in the terminal, one line at a time",
 "mon": "Mon Nov 23",
 "fri": "Fri Nov 13",
 "new": ["changing one slot of a list", "a board stored as a list", "a function that prints a picture",
         "a square number changed into an index", "a test board", "an eight-way gate",
         "taking turns with a remainder", "a loop with two reasons to stop",
         "checking what was typed before using it"],
 "reuse": "Session 3: lists and indexes; session 5: functions that return; session 7: the remainder; session 8: in, and a while loop with two conditions",
 "reuse_note": "One new piece of syntax today: <code>board[4] = \"X\"</code>, which changes one slot of a list. Every other line comes from an earlier session. Tic tac toe is the game on a three by three board where two players take turns putting down X and O, and the first to get three in a row wins. The program is written one line at a time. From chunk 2 on, each new line is a question for the room: What goes next? Each line has hints behind buttons, one inside the next, and the line itself behind the last button. Ask the room before you open anything. Open a hint only when the room is stuck. Open the line last. The game is complete at chunk 7. Chunks 8 and 9 stop a player from taking a square that is already taken.",
 "opener": {
   "title": "Retrieval: in on a list, and a remainder",
   "minutes": 10,
   "body": "Paper first. Then open the editor and make <code>Jonathan_session09.py</code>, with your own first name in place of Jonathan.",
   "questions": [
     {"q": "From session 8. <code>riders</code> is the list <code>[\"Ada\", \"Grace\"]</code>. What does <code>\"Ada\" in riders</code> give, and what does <code>\"Ad\" in riders</code> give?",
      "a": "The first one, <code>\"Ada\" in riders</code>, gives True, because Ada is one of the items in the list. The second one, <code>\"Ad\" in riders</code>, gives False. On a list, <code>in</code> looks for a whole item, and no item is exactly Ad. Today the same test checks whether a square on the board is still free."},
     {"q": "From session 7. <code>colors[i % 3]</code> picked a colour for shape number <code>i</code>. What does <code>5 % 3</code> give, and what are the only three answers <code>i % 3</code> can give?",
      "a": "The first one: <code>5 % 3</code> gives 2, because 3 goes into 5 once with 2 left over. The second one: the only answers are 0, 1, and 2. Today the program divides by 2 instead of 3, so the only answers are 0 and 1, one for each player."},
   ],
 },
 "chunks": [
  {"title": "The board is a list of nine strings",
   "teach": "A tic tac toe board has nine squares, so the program stores it as a list with nine items. Each item is a string. At the start each string is the number of its square, <code>\"1\"</code> to <code>\"9\"</code>, so a player can see which number to type.</p><p>The figure shows both numbers for every square. The big number is the square. The small number is the <b>index</b> of its slot in the list. The list starts counting at 0, so the index is always one less than the square.</p><p>Line 4 is new. You have used <code>board[4]</code> to read a slot. With an equals sign after it, the same brackets <b>change</b> the slot: <code>board[4] = \"X\"</code> throws away what slot 4 held and stores X there. The other eight slots stay as they were.",
   "figure": board_figure(),
   "code": C1,
   "run": "py",
   "predict": "Lines 3 and 5 are the same line, <code>print(board[4])</code>. What does each one print, and which square on the board is slot 4?",
   "reveal": "Line 3 prints 5 and line 5 prints X. Line 4 changed slot 4 between them. Slot 4 is square 5, the middle of the board, because the index is one less than the square. The last line prints the whole list, and you can see X sitting between 4 and 6. If you get an IndexError, the number in the brackets is 9 or more. Nine items means the indexes go from 0 to 8."},

  {"title": "A function that draws the board",
   "teach": "<code>print(board)</code> shows the list on one line, which does not look like a board. This chunk writes a function, <code>show</code>, that prints the nine slots as three rows with lines between them. The game will call it every turn.</p><p>Delete lines 2, 3, 5, and 6 from chunk 1, the four print lines. Keep the two lines that are left. The function goes above them, at the top of the file, with an empty line after it. Python has to read a function before the line that calls it.",
   "start": C2_START,
   "steps": [
     {"label": "Line 1",
      "q": "The function is called <code>show</code> and it needs the board. Which line starts it?",
      "hints": ["A function starts with <code>def</code>, then its name, then parentheses with the parameter inside, then a colon.",
                {"text": "Fill the blank.", "code": 'def show(____):'}],
      "line": 'def show(board):'},
     {"label": "Line 2",
      "q": "The top row shows slots 0, 1, and 2 with an upright bar between them. Which line prints it?",
      "hints": ["One <code>print</code> with an f-string. An f-string can hold a list slot in its braces, like <code>{board[0]}</code>.",
                "A space, then slot 0, then space bar space, then slot 1, then space bar space, then slot 2. To type the bar, hold Shift and press the backslash key, which is above Enter. The line is one indentation level in, because it is inside the function.",
                {"text": "Fill the blanks.", "code": '    print(f" {board[0]} | {board[____]} | {board[____]}")'}],
      "line": '    print(f" {board[0]} | {board[1]} | {board[2]}")'},
     {"label": "Line 3",
      "q": "Under the top row goes a line across the board. Which line prints it?",
      "hints": ["A plain string, with no f and no braces, because nothing in it changes. Three minus signs, a plus sign where the bars cross, three more minus signs, a plus sign, three more.",
                {"text": "Fill the blank.", "code": '    print("---+____+---")'}],
      "line": '    print("---+---+---")'},
     {"label": "Lines 4 to 6",
      "q": "The middle row, another line across, and the bottom row. They are copies of lines 2 and 3 with different numbers. Which slots does each row show?",
      "hints": ["The middle row is slots 3, 4, and 5. The bottom row is slots 6, 7, and 8. Look at the small numbers in the figure in chunk 1.",
                "Copy line 2 twice and line 3 once, then change only the numbers in the brackets.",
                {"text": "Fill the blanks.", "code": '    print(f" {board[3]} | {board[____]} | {board[____]}")\n    print("---+---+---")\n    print(f" {board[____]} | {board[____]} | {board[____]}")'}],
      "line": '    print(f" {board[3]} | {board[4]} | {board[5]}")\n    print("---+---+---")\n    print(f" {board[6]} | {board[7]} | {board[8]}")'},
     {"label": "Line 10",
      "q": "The function is written and nothing has run yet. Which line makes it draw the board?",
      "hints": ["A call: the function's name, then parentheses with the list inside.",
                {"text": "Fill the blank.", "code": 'show(____)'}],
      "line": 'show(board)',
      "note": "It is at the left edge, under <code>board[4] = \"X\"</code>. It is not part of the function. The function's last line is line 6."},
   ],
   "code": C2,
   "run": "py",
   "predict": "Line 9 put X in slot 4 before line 10 called <code>show</code>. Which row of the picture has the X in it, and what is on its left and on its right?",
   "reveal": "The middle row, with 4 on its left and 6 on its right. Line 4 of the function prints slots 3, 4, and 5, and slot 4 holds X. The other eight squares still show their own numbers. If the picture comes out as one row repeated three times, the numbers in the brackets on lines 4 and 6 were not changed after copying."},

  {"title": "One move from the keyboard",
   "teach": "The program put the X in the middle by itself. Now the player picks the square. The player types the number of a square, 1 to 9, and the program has to change that into the index of a slot, 0 to 8.</p><p>Line 9, <code>board[4] = \"X\"</code>, is deleted. Five lines replace it.",
   "steps": [
     {"label": "Line 9",
      "q": "Before the player picks, they need to see the board. Which line shows it?",
      "hints": ["The same call that ended chunk 2.",
                {"text": "Fill the blank.", "code": '____(board)'}],
      "line": 'show(board)',
      "note": "This line takes the place of <code>board[4] = \"X\"</code>."},
     {"label": "Line 10",
      "q": "Which line asks the player for a square and stores what they type?",
      "hints": ["<code>input</code> from session 1, stored under the name <code>move</code>. The text in the parentheses is the question the player sees.",
                {"text": "Fill the blank.", "code": 'move = ____("Player X, pick a square: ")'}],
      "line": 'move = input("Player X, pick a square: ")'},
     {"label": "Line 11",
      "q": "<code>move</code> holds text, like <code>\"7\"</code>. The list needs a whole number, and it needs the index, not the square. Which line makes the index?",
      "hints": ["<code>int(move)</code> changes the type from text to a whole number, the way session 1 did with an age.",
                "The index is one less than the square, so take 1 away. Store the answer under the name <code>spot</code>.",
                {"text": "Fill the blanks.", "code": 'spot = ____(move) - ____'}],
      "line": 'spot = int(move) - 1'},
     {"label": "Line 12",
      "q": "Which line puts X in that slot?",
      "hints": ["Chunk 1's new line, with <code>spot</code> in the brackets where the 4 was.",
                {"text": "Fill the blank.", "code": 'board[____] = "X"'}],
      "line": 'board[spot] = "X"'},
     {"label": "Line 13",
      "q": "The list has changed. The picture on the screen has not. Which line shows the new board?",
      "hints": ["Call <code>show</code> again. A picture that was printed before the change cannot update itself.",
                {"text": "Fill the blank.", "code": 'show(____)'}],
      "line": 'show(board)'},
   ],
   "code": C3,
   "run": "py",
   "stdin": "7\n",
   "predict": "The player types 7. What number does <code>spot</code> hold after line 11, and which corner of the board gets the X?",
   "reveal": "<code>spot</code> holds 6, and the X goes in the bottom left corner. Square 7 is slot 6, the first slot of the bottom row. The board is printed twice: once by line 9 before the move and once by line 13 after it. If the X lands one square to the right of the one you picked, the <code>- 1</code> is missing from line 11."},

  {"title": "Three in a row",
   "teach": "A player wins with three of their marks in a row. Start with the three rows that go across. The top row is slots 0, 1, and 2. If all three hold the same thing, somebody has won, and the thing they hold says who.</p><p>This chunk writes a function, <code>winner</code>, that returns <code>\"X\"</code> or <code>\"O\"</code> if a row is complete, and an empty string if no row is. It goes under <code>show</code>, with an empty line between them, and above the <code>board</code> line.</p><p>Line 18 is a <b>test board</b>. To find out whether <code>winner</code> works you need a board that is one move away from a win, and playing your way there every time is slow. So you type the board you want straight into the list.",
   "steps": [
     {"label": "Line 8",
      "q": "The function is called <code>winner</code> and it needs the board. Which line starts it?",
      "hints": ["The same shape as line 1, with a different name.",
                {"text": "Fill the blank.", "code": 'def ____(board):'}],
      "line": 'def winner(board):',
      "note": "At the left edge, with its own <code>def</code>. It is a second function, not a part of <code>show</code>."},
     {"label": "Line 9",
      "q": "The top row is complete when slots 0, 1, and 2 all hold the same thing. Which line tests that?",
      "hints": ["<code>==</code> compares two things at a time, so three slots need two comparisons: slot 0 with slot 1, and slot 1 with slot 2.",
                "Join the two comparisons with <code>and</code>, so both have to be True.",
                {"text": "Fill the blanks.", "code": '    if board[0] == board[1] ____ board[1] == board[____]:'}],
      "line": '    if board[0] == board[1] and board[1] == board[2]:'},
     {"label": "Line 10",
      "q": "The row is complete. What does the function return, so the caller knows who won?",
      "hints": ["All three slots hold the same mark, so any one of them is the winner's mark.",
                {"text": "Fill the blank. Two indentation levels in.", "code": '        return board[____]'}],
      "line": '        return board[0]'},
     {"label": "Lines 11 to 14",
      "q": "The middle row and the bottom row get the same test. What changes?",
      "hints": ["Each one is another way through the gate, so each starts with <code>elif</code>.",
                "Only the slot numbers change: 3, 4, 5 for the middle row and 6, 7, 8 for the bottom row. Each <code>return</code> gives back a slot from its own row.",
                {"text": "Fill the blanks.", "code": '    elif board[3] == board[4] and board[4] == board[____]:\n        return board[3]\n    elif board[6] == board[____] and board[____] == board[8]:\n        return board[____]'}],
      "line": '    elif board[3] == board[4] and board[4] == board[5]:\n        return board[3]\n    elif board[6] == board[7] and board[7] == board[8]:\n        return board[6]'},
     {"label": "Lines 15 and 16",
      "q": "No row is complete. What does the function return then?",
      "hints": ["Every other case is the <code>else</code>, lined up with the <code>if</code>.",
                "An empty string: two quote marks with nothing between them. It means nobody has won.",
                {"text": "Fill the blank.", "code": '    else:\n        return ____'}],
      "line": '    else:\n        return ""'},
     {"label": "Line 18",
      "q": "To test the function you need a board where X has two in the top row and O has two in the middle row. What does the list look like?",
      "hints": ["Slots 0 and 1 hold X. Slots 3 and 4 hold O. Every other slot still holds its own square number.",
                {"text": "Fill the blanks.", "code": 'board = ["X", "X", "3", ____, ____, "6", "7", "8", "9"]'}],
      "line": ROW_TEST,
      "note": "Change the <code>board</code> line you already have. Do not add a second one."},
     {"label": "Line 24",
      "q": "After the move, the program should say what <code>winner</code> returns. Which line prints it?",
      "hints": ["A call to <code>winner</code> inside the braces of an f-string. The call turns into the string the function returns.",
                {"text": "Fill the blank.", "code": 'print(f"winner: {____(board)}")'}],
      "line": 'print(f"winner: {winner(board)}")',
      "note": "The last line of the file, at the left edge."},
   ],
   "code": C4,
   "run": "py",
   "stdin": "3\n",
   "predict": "On the test board, player X types 3. Which line of <code>winner</code> returns, and what does line 24 print? Then say what line 24 would print if X typed 9 instead.",
   "reveal": "With 3: line 10 returns, and line 24 prints <code>winner: X</code>. Slots 0, 1, and 2 all hold X, so the test on line 9 is True and the function returns slot 0, which is X.</p><p>With 9: line 24 prints <code>winner:</code> with nothing after it. No row is complete, so the <code>else</code> returns the empty string. Run it again and type 9 to see it. An empty board can never look like a win, because every free square holds a different number, so three free squares are never the same.</p><p>If line 24 prints <code>winner: None</code>, a <code>return</code> is missing."},

  {"title": "Eight ways to win",
   "teach": "Three rows are not the only lines of three. There are three columns that go down and two diagonals that go from corner to corner. That makes eight ways to win, and the figure shows the three slots in each one.</p><p><code>winner</code> gets five more ways through its gate. They go between the bottom row's <code>return</code> on line 14 and the <code>else</code>.",
   "figure": lines_figure(),
   "steps": [
     {"label": "Lines 15 and 16",
      "q": "The left column is slots 0, 3, and 6. Which two lines test it and return the winner?",
      "hints": ["The same shape as a row: <code>elif</code>, two comparisons joined by <code>and</code>, then a <code>return</code>.",
                {"text": "Fill the blanks.", "code": '    elif board[0] == board[3] and board[3] == board[____]:\n        return board[____]'}],
      "line": '    elif board[0] == board[3] and board[3] == board[6]:\n        return board[0]'},
     {"label": "Lines 17 to 20",
      "q": "The middle column and the right column. Which slots are in each?",
      "hints": ["Read them from the figure: 1, 4, 7 and 2, 5, 8. Going down a column adds 3 to the slot each time.",
                {"text": "Fill the blanks.", "code": '    elif board[1] == board[4] and board[4] == board[____]:\n        return board[1]\n    elif board[2] == board[____] and board[____] == board[8]:\n        return board[2]'}],
      "line": '    elif board[1] == board[4] and board[4] == board[7]:\n        return board[1]\n    elif board[2] == board[5] and board[5] == board[8]:\n        return board[2]'},
     {"label": "Lines 21 to 24",
      "q": "The two diagonals. Both go through the middle square. Which slots are in each?",
      "hints": ["One goes from the top left corner to the bottom right: 0, 4, 8. The other goes from the top right corner to the bottom left: 2, 4, 6.",
                {"text": "Fill the blanks.", "code": '    elif board[0] == board[4] and board[4] == board[____]:\n        return board[0]\n    elif board[2] == board[4] and board[4] == board[____]:\n        return board[____]'}],
      "line": '    elif board[0] == board[4] and board[4] == board[8]:\n        return board[0]\n    elif board[2] == board[4] and board[4] == board[6]:\n        return board[2]'},
     {"label": "Line 28",
      "q": "A new test board: X in the top left corner and the middle, O in squares 2 and 6. What does the list look like?",
      "hints": ["X is in slots 0 and 4. O is in slots 1 and 5. Every other slot holds its own square number.",
                {"text": "Fill the blanks.", "code": 'board = ["X", "O", "3", "4", ____, ____, "7", "8", "9"]'}],
      "line": ALL_TEST,
      "note": "Change the <code>board</code> line again. The <code>else</code> and its <code>return</code> are now lines 25 and 26."},
   ],
   "code": C5,
   "run": "py",
   "stdin": "9\n",
   "predict": "On the new test board, player X types 9. Which three slots make the line of three, and which line of <code>winner</code> returns?",
   "reveal": "Slots 0, 4, and 8, the diagonal from the top left corner to the bottom right. Line 22 returns, and the last line prints <code>winner: X</code>. Python tried the six tests above it first, three rows and three columns, and each one was False.</p><p>Test the other ways before you go on. Change the test board, run it, and check that a column of O prints <code>winner: O</code>. A way to win that was typed with a wrong slot number gives no error. It only fails when a game ends on that line, so test all eight now."},

  {"title": "Taking turns",
   "teach": "The program takes one move and stops. A game is the same lines again and again, with X and O taking turns, until somebody wins or the board is full. That is a <code>while</code> loop with two conditions joined by <code>and</code>.</p><p>A counter, <code>turns</code>, counts the moves made so far. It does two jobs. It stops the loop after nine moves, because the board has nine squares. And it picks the player: <code>turns % 2</code> is the remainder after dividing by 2, which is 0, 1, 0, 1 as <code>turns</code> goes up, and that number is an index into a list of the two marks.</p><p>Put the board back to the nine numbers first, on line 28. Delete the last line, the <code>winner:</code> print.",
   "steps": [
     {"label": "Line 28",
      "q": "The game starts on an empty board. What does the <code>board</code> line go back to?",
      "hints": ["The nine square numbers, as strings, the way chunk 1 had it.",
                {"text": "Fill the blanks.", "code": 'board = ["1", "2", "3", "4", "5", "6", ____, ____, ____]'}],
      "line": EMPTY},
     {"label": "Lines 29 and 30",
      "q": "The game needs a list of the two marks, X first, and a counter for the moves made so far. What are the two lines?",
      "hints": ["The list is called <code>marks</code> and holds two strings. The counter is called <code>turns</code> and starts where every counter since session 3 has started.",
                {"text": "Fill the blanks.", "code": 'marks = ["X", ____]\nturns = ____'}],
      "line": 'marks = ["X", "O"]\nturns = 0'},
     {"label": "Line 31",
      "q": "The loop keeps going while there are moves left and nobody has won. Which line says both?",
      "hints": ["A <code>while</code> with two tests joined by <code>and</code>. Both have to be True for another turn.",
                "First test: fewer than nine moves so far. Second test: <code>winner(board)</code> is the empty string, which is what it returns when nobody has won. A call can sit inside a condition, because the call turns into the string the function returns.",
                {"text": "Fill the blanks.", "code": 'while turns < ____ and winner(board) == ____:'}],
      "line": 'while turns < 9 and winner(board) == "":'},
     {"label": "Line 32",
      "q": "Each turn starts by showing the board. What happens to the <code>show(board)</code> line you already have?",
      "hints": ["It moves inside the loop: one indentation level in, under the <code>while</code> line.",
                {"text": "Fill the blank.", "code": '    ____(board)'}],
      "line": '    show(board)'},
     {"label": "Line 33",
      "q": "Whose turn is it? Which line picks X when <code>turns</code> is 0, 2, 4 and O when it is 1, 3, 5?",
      "hints": ["<code>turns % 2</code> gives 0 for an even number and 1 for an odd number.",
                "Use that as the index into <code>marks</code>, and store the mark under the name <code>player</code>.",
                {"text": "Fill the blank.", "code": '    player = marks[turns % ____]'}],
      "line": '    player = marks[turns % 2]'},
     {"label": "Line 34",
      "q": "The question said Player X every time. How does it name the right player now?",
      "hints": ["Make the string an f-string and put <code>player</code> in braces where the X was.",
                {"text": "Fill the blank.", "code": '    move = input(f"Player {____}, pick a square: ")'}],
      "line": '    move = input(f"Player {player}, pick a square: ")'},
     {"label": "Lines 35 and 36",
      "q": "The index line stays as it was, one indentation level in. The next line put X in the slot every time. What goes in the slot now?",
      "hints": ["The mark of the player whose turn it is. The name <code>player</code> holds it.",
                {"text": "Fill the blank.", "code": '    spot = int(move) - 1\n    board[spot] = ____'}],
      "line": '    spot = int(move) - 1\n    board[spot] = player'},
     {"label": "Line 37",
      "q": "One move has been made. Which line makes the next turn belong to the other player?",
      "hints": ["Add 1 to the counter. The next pass works out <code>turns % 2</code> again and gets the other index.",
                {"text": "Fill the blank.", "code": '    turns = turns ____ 1'}],
      "line": '    turns = turns + 1',
      "note": "Without this line the loop never ends and X plays every turn."},
     {"label": "Line 39",
      "q": "The loop has stopped. The last move is in the list. Is it on the screen?",
      "hints": ["No. The board was shown at the start of the turn, before the move. Show it once more, at the left edge, after the loop, with an empty line above.",
                {"text": "Fill the blank.", "code": 'show(____)'}],
      "line": 'show(board)'},
   ],
   "code": C6,
   "run": "py",
   "stdin": "1\n5\n2\n9\n3\n",
   "predict": "The players type 1, 5, 2, 9, 3, taking turns, X first. Which squares does X get, how many times does the loop run, and does O get a turn after X's third move?",
   "reveal": "X gets squares 1, 2, and 3, which is the top row. The loop runs five times. O does not get another turn: before every pass Python checks the <code>while</code> line again, and after the fifth move <code>winner(board)</code> returns X, which is not the empty string, so the condition is False and Python goes to line 39.</p><p>Look at the order of the players in the output: X, O, X, O, X. <code>turns</code> was 0, 1, 2, 3, 4, and <code>turns % 2</code> was 0, 1, 0, 1, 0.</p><p>The program shows the final board and then says nothing. The next chunk adds the last four lines."},

  {"title": "Who won?",
   "teach": "The loop stops for one of two reasons: somebody won, or nine moves were made and the board is full. A full board with no line of three is a <b>draw</b>. One gate after the loop says which it was.",
   "steps": [
     {"label": "Lines 40 and 41",
      "q": "After the loop, how can the program tell that nobody won, and what does it print?",
      "hints": ["Ask <code>winner</code> again. If it returns the empty string, no line of three is on the board.",
                {"text": "Fill the blank.", "code": 'if winner(board) == ____:\n    print("Nobody wins. It is a draw.")'}],
      "line": 'if winner(board) == "":\n    print("Nobody wins. It is a draw.")',
      "note": "At the left edge, straight under the last <code>show(board)</code>."},
     {"label": "Lines 42 and 43",
      "q": "In every other case somebody won. Which two lines say who?",
      "hints": ["An <code>else</code>, then a print. <code>winner(board)</code> returns the winner's mark, and a call can go inside the braces of an f-string.",
                {"text": "Fill the blank.", "code": 'else:\n    print(f"{____(board)} wins!")'}],
      "line": 'else:\n    print(f"{winner(board)} wins!")'},
   ],
   "code": C7,
   "run": "py",
   "stdin": "1\n2\n3\n5\n4\n6\n8\n7\n9\n",
   "predict": "This time the players type 1, 2, 3, 5, 4, 6, 8, 7, 9. All nine squares get filled and nobody gets three in a row. Which of the two conditions on the <code>while</code> line stops the loop, and what is the last line the program prints?",
   "reveal": "<code>turns &lt; 9</code> stops it. After the ninth move <code>turns</code> is 9, and 9 is not less than 9. The other condition was still True, because <code>winner(board)</code> was still returning the empty string. The last line printed is <code>Nobody wins. It is a draw.</code></p><p>The gate checks for a winner, not for a full board, and that matters. If the ninth move completes a line of three, the board is full and somebody has won. <code>winner(board)</code> returns their mark, so the <code>else</code> runs and the program names the winner.</p><p>The game is finished. Play it with the person next to you: one of you is X and the other is O."},

  {"title": "A square that is already taken",
   "teach": "Play a game and try this: X takes square 5, then O types 5 too. The program puts O on top of X. It also stops with an error if a player types a word, or a number over 9.</p><p>The program should check what the player typed before it uses it. Here is a test that does it in one line. A free square still holds its own number as a string. So the thing the player typed is located in the list only if that square is free. That is session 8's <code>in</code>, on a list.</p><p>Lines 35 to 37 move inside a gate, and a turn only counts when the gate lets the move through.",
   "steps": [
     {"label": "Line 35",
      "q": "Which test is True only when the player typed the number of a free square?",
      "hints": ["<code>in</code>, with what the player typed on the left and the list on the right.",
                "If the player types 5 and slot 4 still holds <code>\"5\"</code>, the test is True. If slot 4 holds X or O, there is no <code>\"5\"</code> anywhere in the list, and the test is False.",
                {"text": "Fill the blank.", "code": '    if move ____ board:'}],
      "line": '    if move in board:',
      "note": "A new line, between the <code>input</code> line and the <code>spot</code> line."},
     {"label": "Lines 36 to 38",
      "q": "The three lines that make the move were written to run every turn. What has to happen to them?",
      "hints": ["They move inside the gate: one more indentation level, so they are two levels in.",
                "All three move, the counter too. A turn that was refused must not add 1 to <code>turns</code>, or the player would lose their turn.",
                {"text": "The first line, moved. The other two follow the same way.", "code": '        spot = int(move) - 1'}],
      "line": '        spot = int(move) - 1\n        board[spot] = player\n        turns = turns + 1',
      "note": "In VS Code, select the three lines and press Tab once."},
     {"label": "Lines 39 and 40",
      "q": "What happens when the test is False?",
      "hints": ["An <code>else</code>, lined up with the <code>if</code>, and a print that tells the player to try again.",
                "Nothing else is needed. <code>turns</code> did not change, so the next pass of the loop asks the same player again.",
                {"text": "Fill the blank.", "code": '    ____:\n        print("That is not a free square. Try again.")'}],
      "line": '    else:\n        print("That is not a free square. Try again.")'},
   ],
   "code": C8,
   "run": "py",
   "stdin": "5\n5\nhello\nX\n",
   "predict": "X types 5. Then O types 5, then hello, then the capital letter X. The first two are refused. Slot 4 holds X by then, so what does <code>\"X\" in board</code> give, and what does line 36 do with it?",
   "reveal": "<code>\"X\" in board</code> gives True, because X is one of the items in the list. So the gate lets the move through, and line 36 runs <code>int(\"X\")</code>. Python cannot change X into a whole number, and the program stops with a ValueError. Read the last line of the error in the output box: it shows the X that Python could not use.</p><p>The 5 and the hello were both refused, and O was asked again each time, because neither of them was in the list. The test works for every wrong answer except two: the marks themselves, once they are on the board. The next chunk fixes that."},

  {"title": "A letter instead of a number",
   "teach": "The bug in chunk 8 is in the order of the questions. Before the program asks whether <code>move</code> is in the list, it has to ask whether the player typed a mark. The gate becomes a three-way gate: a mark, a free square, or anything else.",
   "steps": [
     {"label": "Lines 35 and 36",
      "q": "The first case: the player typed X or O. Which test catches both, and what does the program say?",
      "hints": ["Two comparisons joined by <code>or</code>, so either one being True is enough.",
                {"text": "Fill the blanks.", "code": '    if move == "X" ____ move == ____:\n        print("Type the number of a square, not a mark.")'}],
      "line": '    if move == "X" or move == "O":\n        print("Type the number of a square, not a mark.")',
      "note": "Two new lines, between the <code>input</code> line and the <code>in</code> test."},
     {"label": "Line 37",
      "q": "The <code>in</code> test used to be the first question in the gate. It is the second one now. What is the one word that changes?",
      "hints": ["A second way through a gate starts with <code>elif</code>, not <code>if</code>.",
                {"text": "Fill the blank.", "code": '    ____ move in board:'}],
      "line": '    elif move in board:',
      "note": "With <code>if</code> here it would be a second gate, and the <code>else</code> would belong to it. A player who typed X would get both messages."},
   ],
   "code": C9,
   "run": "py",
   "stdin": "5\nX\n5\n1\n4\n2\n6\n",
   "predict": "X types 5. O types the letter X, then 5, then 1. After that X types 4, O types 2, and X types 6. How many of the seven things typed count as a turn, and who wins?",
   "reveal": "Five count as a turn: 5, 1, 4, 2, and 6. The letter X is caught by line 35 and the second 5 is caught by the <code>else</code>, and neither adds 1 to <code>turns</code>, so O is asked three times in a row. X wins with squares 4, 5, and 6, the middle row.</p><p>The order of the branches is what fixed the bug. Python takes the first branch whose test is True and skips the rest, so a typed X never reaches the <code>in</code> test."},
 ],
 "hinge": {"q": "From session 7: the remainder. Line 33 is <code>player = marks[turns % 2]</code>. Six moves have been made, so <code>turns</code> is 6. Whose turn is it? Then say why this line can never ask for <code>marks[2]</code>, which does not exist.",
           "a": "The first part: it is X's turn. 6 divided by 2 leaves a remainder of 0, and <code>marks[0]</code> is X. The second part: the remainder after dividing by 2 is always 0 or 1. If 2 were left over, 2 would go in one more time. So the index always fits a list of two items, whatever number <code>turns</code> has reached."},
 "brief": {
   "title": "Build: test it, then put names on it",
   "minutes": 15,
   "intro": "You have a game two people can play. Before you hand a game to somebody else, you test every way it can end, and tic tac toe can end nine ways: eight lines of three, and a draw. After that you make it yours. The program calls the players X and O. A game on your machine should ask who is playing and use their names.",
   "steps": [
     "Fill in the Expected column of the sheet below. Then play with the person next to you until every row has something in the Got column.",
     "Ask for two names before the game starts. Under the <code>marks</code> line, write <code>name_x = input(\"Who plays X? \")</code>, then the same for <code>name_o</code>, then put both in a list in the same order as the marks: <code>names = [name_x, name_o]</code>.",
     "<code>marks[turns % 2]</code> picks the mark for this turn. The same index picks the name: <code>names[turns % 2]</code>. Store it under <code>name</code>, and change the question on the <code>input</code> line so it uses the name and the mark, like <code>Ada (X), pick a square:</code>",
     "Change the last line so it says the winner's name. <code>winner(board)</code> returns the mark, not the name, so the gate after the loop needs three ways through: a draw, X won so print <code>names[0]</code>, and every other case, where O won, so print <code>names[1]</code>.",
     "Play one more game against your partner with the names in.",
   ],
   "expected_got": [
     ["Three X in a row across: what is the last line printed?", ""],
     ["Three O in a column going down: what is the last line printed?", ""],
     ["Three in a diagonal: does the game stop on that move?", ""],
     ["All nine squares full and no line of three: what is the last line printed?", ""],
     ["A player types the number of a taken square: who is asked next?", ""],
     ["A player types X: does the program stop with an error?", ""],
   ],
 },
 "exits": {
   "floor": "The board, <code>show</code>, and one move from the keyboard that lands in the right square (chunk 3).",
   "middle": "The two-player game from chunk 7: players take turns, the game stops on a line of three or a full board, and the last line says who won or that it is a draw.",
   "stretch": "The game from chunk 9, which refuses a taken square and a typed mark, with the players' names in the question and in the last line.",
 },
 "extension": {
   "title": "Play against the computer",
   "intro": "<p>For a player with nobody to play against. The computer takes O and picks its square at random with <code>random.choice</code> from session 4. It does not try to win or to block you. It only has to pick a square that is free.</p><p>The two functions do not change. Add <code>import random</code> as the first line of the file, with an empty line under it, and change the game part of the program to the lines below.</p>",
   "cards": [
     {"title": "The computer picks until it finds a free square",
      "teach": "<code>random.choice(board)</code> gives back one of the nine items in the list. If the square is free, the item is its number, and that is a move the program already knows how to make. If the square is taken, the item is X or O, and the computer has to pick again. A <code>while</code> loop keeps picking until the pick is not a mark.",
      "next": {"q": "On the computer's turn, <code>move</code> does not come from the keyboard. Which lines give <code>move</code> a value, and which lines keep going until that value is a free square?",
               "hints": ["A gate on <code>player</code>: if it is X, ask the keyboard with <code>input</code>, as before. In every other case, pick with <code>random.choice(board)</code>.",
                         "Under the pick, a <code>while</code> loop whose condition is the same test as chunk 9's first branch: <code>move == \"X\" or move == \"O\"</code>. Its block picks again. The loop ends when the pick is a number.",
                         {"text": "Fill the blanks.", "code": '    else:\n        move = random.____(board)\n        while move == "X" ____ move == "O":\n            move = random.choice(____)'}],
               "a": "The gate on <code>player</code> is new, and so is the loop inside its <code>else</code>. The three-way gate from chunk 9 follows it and is not changed. It is a second gate under the first one, not a gate inside a gate: both start one indentation level in."},
      "code": COMPUTER,
      "prefix": "import random\n\n" + FUNCTIONS,
      "run": "py",
      "seed": 4,
      "stdin": "5\n1\n9\n",
      "predict": "The computer's first pick is always a free square, with no second try. Later picks sometimes need several tries. Why is the first one different?",
      "reveal": "On an empty board all nine items are numbers, so whatever <code>random.choice</code> gives back is a free square, and the <code>while</code> condition is False the first time it is checked. When the computer first plays, one square holds your X, so one item in nine is a mark. Later in the game most of the items are marks, and the loop may run several times before a number comes up. You do not see the tries, because the print is after the loop, not inside it.</p><p>The output box shows one game. Your game will differ, because the computer picks again every run."},
   ],
   "steps": [
     "Add <code>import random</code> at the top of the file and change the game part to the lines on the card.",
     "Play three games. The computer plays badly, because it picks at random. Write down how many of the three you won.",
     "Put a probe inside the computer's <code>while</code> loop: <code>print(f\"tried {move}\")</code> as the first line of its block. Play again and count the tries on the computer's last turn.",
     "Let the computer go first: make it play X and you play O. One comparison on the <code>if player ==</code> line changes, and so does the text of the question.",
   ],
   "checks": [
     "The computer never takes a square that already holds a mark",
     "After your move the computer moves without being asked",
     "If you type a taken square, you are asked again and the computer does not move",
     "With the probe in, the number of tries goes up as the board fills",
   ],
 },
 "ledger": "Stamp 9: <code>board[4] = \"X\"</code> changes one slot of a list, the index is the square minus 1, <code>marks[turns % 2]</code> takes turns, <code>move in board</code> is True only for a free square, a function that returns the winner or an empty string, a test board typed straight into the list.",
 "teacher": {
   "timing": [
     "0:00 retrieval opener, 10 min",
     "0:10 chunks 1 to 3, the board and one move, 18 min",
     "0:28 chunks 4 and 5, winner and its test boards, 17 min",
     "0:45 chunks 6 and 7, turns and the verdict, 15 min",
     "1:00 chunks 8 and 9, refusing a bad move, 10 min",
     "1:10 build brief, test sheet and names, 15 min (note: most rooms finish the test sheet; the names are the stretch)",
     "1:25 exits, ledger stamp, 5 min",
   ],
   "misconceptions": [
     ["The X lands one square to the right of the one picked, or square 9 gives an IndexError.", "The <code>- 1</code> is missing from the <code>spot</code> line. Point at the figure in chunk 1: the big number is what the player types, the small number is what the list needs."],
     ["Types the eight tests with a slip in one slot number, and the game misses that win or calls a win that is not there.", "There is no error message for this. Have them set a test board for each of the eight lines and read the slot numbers against the figure in chunk 5."],
     ["Writes <code>board[0] == board[1] == board[2]</code>, or <code>board[0] and board[1] and board[2] == \"X\"</code>.", "The first works in Python but is not a shape this course has taught, so ask for the two comparisons joined by <code>and</code>. The second is always True for the first two slots, because any string with something in it counts as True. Print the condition by itself to show it."],
     ["Leaves <code>turns = turns + 1</code> outside the gate in chunk 8, so a refused move still uses up the turn.", "Have them type a taken square and watch whose name comes up next. The counter line belongs with the two lines that make the move."],
     ["Keeps <code>if</code> on the <code>in</code> test in chunk 9 and gets two messages for one typed X.", "Two <code>if</code> lines are two gates. Change the second to <code>elif</code> and run the same input again."],
     ["Indents the last <code>show(board)</code> and the verdict so they are inside the loop.", "The verdict then prints every turn. Lines that run once, after the game, start at the left edge."],
   ],
   "standards": ["MP1", "MP7", "MP8"],
   "routing": "The game is complete at chunk 7, and that is the middle exit. If it runs long, stop the chunks there, play the game in pairs, and use the build's test sheet. Chunks 8 and 9 can be done from the front as a demonstration: type a taken square, then type X, and show the two fixes. The names in the build and the computer player in the extension can both be dropped without loss.",
 },
}
