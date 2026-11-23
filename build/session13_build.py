# Session 13's build, written out one line at a time (added November 2026; it was
# session 12 until the coin grab session took that number).
# Four tools, each a whole program that grows out of the one before:
#   tool 1  the level printed in the terminal            (the floor exit)
#   tool 2  the room in a window and a player that walls stop
#   tool 3  coins and a score                            (tools 2 and 3: the middle exit)
#   tool 4  a trap, three lives, game over, and restart
# Every new line is a What goes next? question; its three choices are in picks.py.
# Each program is run when the site is built, tools 2 to 4 headless with key presses fed in.

LEVEL = '''level = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
]'''

START1 = '''ROWS = 5
COLS = 7

''' + LEVEL

TOOL1 = START1 + '''

for row in range(ROWS):
    line = ""
    for col in range(COLS):
        if level[row][col] == 1:
            line = line + "#"
        else:
            line = line + "."
    print(line)'''

IS_OPEN = '''def is_open(row, col):
    if row < 0:
        return False
    if col < 0:
        return False
    if row > len(level) - 1:
        return False
    if col > len(level[0]) - 1:
        return False
    return level[row][col] == 0'''

TOP2 = '''import pygame

# ---- knob block: every number the game depends on ----
TILE = 64
ROWS = 5
COLS = 7
FPS = 60
BG = (27, 41, 81)
WALL = (110, 120, 150)
FLOOR = (40, 56, 100)
PLAYER = (248, 250, 252)

''' + LEVEL + '''

''' + IS_OPEN + '''

pygame.init()
screen = pygame.display.set_mode((COLS * TILE, ROWS * TILE))
clock = pygame.time.Clock()
'''

START2 = TOP2 + '''
running = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0

    screen.fill(BG)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()'''

TOOL2 = TOP2 + '''
player_row = 1
player_col = 1

running = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        next_row = player_row
        next_col = player_col
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            next_col = player_col + 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            next_col = player_col - 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            next_row = player_row - 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            next_row = player_row + 1
        if is_open(next_row, next_col):
            player_row = next_row
            player_col = next_col

    screen.fill(BG)
    for row in range(ROWS):
        for col in range(COLS):
            box = (col * TILE, row * TILE, TILE, TILE)
            if level[row][col] == 1:
                pygame.draw.rect(screen, WALL, box)
            else:
                pygame.draw.rect(screen, FLOOR, box)
    box = (player_col * TILE, player_row * TILE, TILE, TILE)
    pygame.draw.rect(screen, PLAYER, box)
    pygame.display.flip()
    clock.tick(FPS)

print(f"The player stopped at row {player_row}, column {player_col}.")
pygame.quit()'''


def swap(program, old, new):
    """Replace one piece of a program; the piece has to be there exactly once."""
    assert program.count(old) == 1, old
    return program.replace(old, new)


TOOL3 = TOOL2
TOOL3 = swap(TOOL3, 'PLAYER = (248, 250, 252)\n', 'PLAYER = (248, 250, 252)\nCOIN = (252, 211, 77)\n')
TOOL3 = swap(TOOL3, '    [1, 0, 0, 0, 0, 0, 1],\n    [1, 0, 1, 0, 1, 0, 1],\n    [1, 0, 0, 0, 0, 0, 1],\n',
             '    [1, 0, 0, 0, 0, 2, 1],\n    [1, 0, 1, 0, 1, 0, 1],\n    [1, 2, 0, 0, 0, 0, 1],\n')
TOOL3 = swap(TOOL3, '    return level[row][col] == 0', '    return level[row][col] != 1')
TOOL3 = swap(TOOL3, 'player_col = 1\n', 'player_col = 1\nscore = 0\n')
TOOL3 = swap(TOOL3, '            player_col = next_col\n\n', '''            player_col = next_col

    if level[player_row][player_col] == 2:
        level[player_row][player_col] = 0
        score = score + 1
        print(f"score {score}")

''')
TOOL3 = swap(TOOL3, '                pygame.draw.rect(screen, FLOOR, box)\n', '''                pygame.draw.rect(screen, FLOOR, box)
            if level[row][col] == 2:
                middle = (col * TILE + TILE / 2, row * TILE + TILE / 2)
                pygame.draw.circle(screen, COIN, middle, TILE / 4)
''')

TOOL4 = TOOL3
TOOL4 = swap(TOOL4, 'COIN = (252, 211, 77)\n', 'COIN = (252, 211, 77)\nTRAP = (220, 38, 38)\nLIVES = 3\n')
TOOL4 = swap(TOOL4, '    [1, 2, 0, 0, 0, 0, 1],\n', '    [1, 2, 0, 0, 0, 3, 1],\n')
TOOL4 = swap(TOOL4, '    return level[row][col] != 1\n', '''    return level[row][col] != 1

def new_game():
    return "play", LIVES, 0
''')
TOOL4 = swap(TOOL4, 'player_col = 1\nscore = 0\n', 'player_col = 1\nstate, lives, score = new_game()\n')
TOOL4 = swap(TOOL4, '        if is_open(next_row, next_col):\n            player_row = next_row\n            player_col = next_col\n',
             '''        if state == "play" and is_open(next_row, next_col):
            player_row = next_row
            player_col = next_col
''')
TOOL4 = swap(TOOL4, '    if level[player_row][player_col] == 2:\n', '''    keys = pygame.key.get_pressed()
    if state == "over" and keys[pygame.K_r]:
        state, lives, score = new_game()
        player_row = 1
        player_col = 1

    if level[player_row][player_col] == 2:
''')
TOOL4 = swap(TOOL4, '        print(f"score {score}")\n', '''        print(f"score {score}")
    if state == "play" and level[player_row][player_col] == 3:
        lives = lives - 1
        player_row = 1
        player_col = 1
        print(f"hit! lives {lives}")
    if state == "play" and lives == 0:
        state = "over"
        print(f"game over, final score {score}")
''')
TOOL4 = swap(TOOL4, '                pygame.draw.circle(screen, COIN, middle, TILE / 4)\n', '''                pygame.draw.circle(screen, COIN, middle, TILE / 4)
            if level[row][col] == 3:
                pygame.draw.rect(screen, TRAP, box)
''')


def step(program, q, block, note=None, nth=1, part2=None):
    """One What goes next? step: the lines it adds, and a label worked out from the program.

    block is one or more whole lines that sit together in the program. nth picks
    which copy when the same lines appear more than once. part2 is a second line
    somewhere else in the program, for a step that changes two lines that are apart.
    """
    lines = program.split("\n")
    want = block.split("\n")
    starts = [i for i in range(len(lines)) if lines[i:i + len(want)] == want]
    assert len(starts) >= nth, "not in the program: " + block
    first = starts[nth - 1] + 1
    last = first + len(want) - 1
    line = block
    if part2:
        assert len(want) == 1 and lines.count(part2) == 1, part2
        label = "Lines %d and %d" % (first, lines.index(part2) + 1)
        line = block + "\n" + part2
    elif len(want) == 1:
        label = "Line %d" % first
    elif len(want) == 2:
        label = "Lines %d and %d" % (first, last)
    else:
        label = "Lines %d to %d" % (first, last)
    out = {"label": label, "q": q, "line": line}
    if note:
        out["note"] = note
    return out


def presses(*names):
    """Key presses for the headless run: one every third frame, starting on frame 3."""
    return [[3 * (k + 1), "KEYDOWN", "K_" + name] for k, name in enumerate(names)]


TRIP = ["RIGHT", "RIGHT", "RIGHT", "RIGHT", "DOWN", "DOWN"]

TOOLS13 = [
    {"title": "Tool 1: the level in the terminal",
     "intro": "Before the window, print the room in the terminal: one line of text for each row of the level, with <code>#</code> for a wall and <code>.</code> for floor. The two knobs and the level are given. Copy them from the button below, then write the loop under them.",
     "start": START1,
     "whole": "Show the whole program",
     "code": TOOL1,
     "run": "py",
     "steps": [
         step(TOOL1, "The room has one line of text for each row. Which line visits every row?",
              'for row in range(ROWS):', note="At the left edge, under the level, with an empty line above."),
         step(TOOL1, "Each row is built as one string, one character at a time. What does the string start as?",
              '    line = ""'),
         step(TOOL1, "Inside a row, which line visits every column?",
              '    for col in range(COLS):'),
         step(TOOL1, "A wall tile is a 1. Which test finds a wall, and what is added to the line?",
              '        if level[row][col] == 1:\n            line = line + "#"'),
         step(TOOL1, "What is added for every tile that is not a wall?",
              '        else:\n            line = line + "."'),
         step(TOOL1, "The row is built. Which line prints it?",
              '    print(line)'),
     ],
     "predict": "How many lines print, and what is the middle line?",
     "reveal": "Five lines, one for each row of the level. The middle line is <code>#.#.#.#</code>, because row 2 has a wall in columns 0, 2, 4, and 6. This is the floor exit.",
     },
    {"title": "Tool 2: the room and the player",
     "intro": "Now the window. Keep <code>ROWS</code>, <code>COLS</code>, and the level, and delete tool 1's printing loop. Then make your file match the program behind the button below. It has the knob block, the level, <code>is_open</code> from chunk 3, and the frame loop from session 11. Run it and check that an empty window opens. Then add the lines below, one question at a time.",
     "start": START2,
     "whole": "Show the whole program",
     "code": TOOL2,
     "run": "headless", "frames": 40,
     "inject": presses("RIGHT", "RIGHT", "RIGHT", "DOWN", "RIGHT", "DOWN", "DOWN", "DOWN"),
     "steps": [
         step(TOOL2, "The player stands on one tile, and two variables hold which one. Tile row 1, column 1 is open floor. What are the two lines?",
              'player_row = 1\nplayer_col = 1', note="Under the <code>clock</code> line, with an empty line above."),
         step(TOOL2, "On every frame, every tile is drawn. Which two lines visit every tile?",
              '    for row in range(ROWS):\n        for col in range(COLS):',
              note="Under <code>screen.fill(BG)</code>, one indentation level in."),
         step(TOOL2, "A tile is a square, <code>TILE</code> wide and <code>TILE</code> tall. Where is its left edge, and where is its top edge?",
              '            box = (col * TILE, row * TILE, TILE, TILE)'),
         step(TOOL2, "Wall tiles and floor tiles get different colours. Which gate picks the colour?",
              '            if level[row][col] == 1:\n                pygame.draw.rect(screen, WALL, box)\n            else:\n                pygame.draw.rect(screen, FLOOR, box)'),
         step(TOOL2, "The player is a square on its tile. Which two lines draw it?",
              '    box = (player_col * TILE, player_row * TILE, TILE, TILE)\n    pygame.draw.rect(screen, PLAYER, box)',
              note="After the two loops, lined up with the first <code>for</code>, above <code>pygame.display.flip()</code>. Run the program now. It shows the room and a white square."),
         step(TOOL2, "A key press does not move the player straight away. First the program works out which tile the player would go to. What do <code>next_row</code> and <code>next_col</code> start as?",
              '        next_row = player_row\n        next_col = player_col',
              note="Inside the <code>for event</code> loop, lined up with <code>if event.type == pygame.QUIT:</code>."),
         step(TOOL2, "The right arrow is pressed. Which test catches one press, and what happens to the next column?",
              '        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:\n            next_col = player_col + 1'),
         step(TOOL2, "The other three arrows get the same two lines. What changes for left, up, and down?",
              '        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:\n            next_col = player_col - 1\n        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:\n            next_row = player_row - 1\n        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:\n            next_row = player_row + 1'),
         step(TOOL2, "The next tile is worked out. When is the player allowed to move there?",
              '        if is_open(next_row, next_col):\n            player_row = next_row\n            player_col = next_col'),
         step(TOOL2, "When the window closes, the terminal says where the player stopped. Which line prints it?",
              'print(f"The player stopped at row {player_row}, column {player_col}.")',
              note="After the loop, at the left edge, above <code>pygame.quit()</code>."),
     ],
     "predict": "The keys pressed are right, right, right, down, right, down, down, down. Which presses do not move the player, and where does the player stop?",
     "reveal": "Two presses do not move the player. The first down is pressed at row 1, column 4, and <code>level[2][4]</code> is a wall. The last down is pressed at row 3, column 5, and <code>level[4][5]</code> is a wall. The player stops at row 3, column 5.",
     },
    {"title": "Tool 3: coins and a score",
     "intro": "A coin is a third tile value. The player walks onto it, the score goes up by 1, and the coin is gone. The score is printed in the terminal.",
     "start": TOOL2,
     "whole": "Show the whole program",
     "code": TOOL3,
     "run": "headless", "frames": 40,
     "inject": presses("RIGHT", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "LEFT", "RIGHT"),
     "steps": [
         step(TOOL3, "A coin needs a colour, and the colour needs a name in the knob block. Which line adds it?",
              'COIN = (252, 211, 77)', note="Under the <code>PLAYER</code> line."),
         step(TOOL3, "A coin is tile value 2. Put one coin at row 1, column 5 and one at row 3, column 1. What do the two rows look like?",
              '    [1, 0, 0, 0, 0, 2, 1],', part2='    [1, 2, 0, 0, 0, 0, 1],'),
         step(TOOL3, "<code>is_open</code> says a tile is open only when it is 0. A coin tile is 2, so the player could not step on it. Which change to the last line fixes that?",
              '    return level[row][col] != 1'),
         step(TOOL3, "The score needs a starting value. Which line?",
              'score = 0', note="Under <code>player_col = 1</code>."),
         step(TOOL3, "After the events, the program checks the tile the player is standing on. Which test is True when that tile is a coin?",
              '    if level[player_row][player_col] == 2:',
              note="After the <code>for event</code> loop, one indentation level in, above <code>screen.fill(BG)</code>."),
         step(TOOL3, "The player is on a coin. What three things happen?",
              '        level[player_row][player_col] = 0\n        score = score + 1\n        print(f"score {score}")'),
         step(TOOL3, "A coin tile is drawn as floor with a yellow circle in the middle. Where is the middle of a tile?",
              '            if level[row][col] == 2:\n                middle = (col * TILE + TILE / 2, row * TILE + TILE / 2)\n                pygame.draw.circle(screen, COIN, middle, TILE / 4)',
              note="Under the wall and floor gate, lined up with its <code>if</code>. It is a second gate, so a coin tile is drawn as floor first and then gets its circle."),
     ],
     "predict": "The keys pressed are right, right, right, right, right, left, right. The player walks onto the coin tile twice. How many times does the terminal print a score?",
     "reveal": "Once. The fourth press puts the player on the coin at row 1, column 5, and the score goes to 1. The coin gate changes that tile to 0, so when the player steps off and back on, there is no coin left. The fifth press does nothing, because column 6 is a wall. This is the middle exit.",
     },
    {"title": "Tool 4: a trap, three lives, game over, and restart",
     "intro": "The room gets one trap tile. Stepping on it costs a life and sends the player back to the start. When the last life is gone the game is over, the arrow keys stop working, and the R key starts a new game. The state, the lives, and the score come from chunk 6's <code>new_game</code>.",
     "start": TOOL3,
     "whole": "Show the whole program",
     "code": TOOL4,
     "run": "headless", "frames": 80,
     "inject": presses(*(TRIP + TRIP + TRIP + ["RIGHT", "r", "RIGHT"])),
     "steps": [
         step(TOOL4, "The trap needs a colour and the lives need a starting number. Both get a name in the knob block. What number does <code>LIVES</code> hold?",
              'TRAP = (220, 38, 38)\nLIVES = 3', note="Under the <code>COIN</code> line."),
         step(TOOL4, "A trap is tile value 3. Put one at row 3, column 5. What does row 3 look like?",
              '    [1, 2, 0, 0, 0, 3, 1],'),
         step(TOOL4, "Which gate draws a trap tile so the player can see it?",
              '            if level[row][col] == 3:\n                pygame.draw.rect(screen, TRAP, box)',
              note="Under the coin gate in the drawing loops, lined up with its <code>if</code>."),
         step(TOOL4, "Chunk 6's <code>new_game</code> returns three starting values: the state, the lives, and the score. What does it return here?",
              'def new_game():\n    return "play", LIVES, 0',
              note="Under <code>is_open</code>, at the left edge, with an empty line above and below."),
         step(TOOL4, "The line <code>score = 0</code> is replaced. Which one line gives <code>state</code>, <code>lives</code>, and <code>score</code> their starting values?",
              'state, lives, score = new_game()'),
         step(TOOL4, "When the game is over, the arrow keys must not move the player. What is added to the movement gate?",
              '        if state == "play" and is_open(next_row, next_col):'),
         step(TOOL4, "After the coin gate, the program checks for the trap. Which test is True when the player is standing on it?",
              '    if state == "play" and level[player_row][player_col] == 3:',
              note="Under the coin gate, lined up with its <code>if</code>."),
         step(TOOL4, "The player is on the trap. What happens?",
              '        lives = lives - 1\n        player_row = 1\n        player_col = 1\n        print(f"hit! lives {lives}")'),
         step(TOOL4, "When is the game over, and what changes then?",
              '    if state == "play" and lives == 0:\n        state = "over"\n        print(f"game over, final score {score}")'),
         step(TOOL4, "The game is over. The R key starts a new one. Which lines do it?",
              '    keys = pygame.key.get_pressed()\n    if state == "over" and keys[pygame.K_r]:\n        state, lives, score = new_game()\n        player_row = 1\n        player_col = 1',
              note="After the <code>for event</code> loop, one indentation level in, above the coin gate, with an empty line after it."),
     ],
     "predict": "The player walks right four times and down twice, and does that three times over. Then the keys are right, R, right. How many times does the terminal print hit, and which of the last three presses does nothing?",
     "reveal": "Three times, once at the end of each trip: lives 2, lives 1, lives 0. On the third hit the game-over gate runs on the same frame and prints the final score. The right arrow after that does nothing, because the state is <code>\"over\"</code>. R starts a new game, and the last right arrow moves the player one tile, to row 1, column 2. The score printed only once, because the coin was collected on the first trip.",
     },
]
