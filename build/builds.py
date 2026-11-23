# The builds of sessions 1, 2, 3, 4, 6, 7, 9, 10, 11 and the two extra pages, written
# out one line at a time (added November 2026). Sessions 5, 8, 12 and 13 have theirs in
# their own generators. Session 14 is a commission on a finished program, so it has none.
#
# Each build is one or two tools. A tool is a whole program; every new line is a
# What goes next? question with a blank and three choices, kept here beside the step.
# Line labels are worked out from the program, every program is run when the site is
# built, and render.py checks each choice against the step's line.

import session06 as s6
import session09 as s9


def Q(program, q, block, blank, right, wrong1, wrong2, why, note=None, part2=None, nth=1):
    """One What goes next? step, with its label worked out and its three choices.

    block is one or more whole lines that sit together in the program; nth picks
    which copy when they appear more than once. part2 is a second line somewhere
    else, for a step that changes two lines that are apart. blank is the same lines
    with ____ where the choices go.
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
    out = {"label": label, "q": q, "line": line,
           "pick": {"blank": blank, "right": right, "wrong": [wrong1, wrong2], "why": why}}
    if note:
        out["note"] = note
    return out


def swap(program, old, new):
    """Replace one piece of a program; the piece has to be there exactly once."""
    assert program.count(old) == 1, old
    return program.replace(old, new)


HOW = ("Each new line is a question for the room before it goes on the screen. Each question "
       "shows the line with a blank and three choices. Ask the room to pick before you click.")

# ------------------------------------------------------------------ session 1, the rider card

P1 = '''name = input("Rider name: ")
height = input("Height in inches: ")
height = int(height)
tickets = input("How many tickets: ")
tickets = int(tickets)
print(f"{name} is {height} inches tall and has {tickets} tickets.")
tickets = tickets + 1
print(f"With one more, {name} has {tickets} tickets.")'''

# ------------------------------------------------------------------ session 2, the ride operator

P2 = '''height = input("Height in inches: ")
height = int(height)
ticket = ""
while ticket != "yes" and ticket != "no":
    ticket = input("Do you have a ticket? Type yes or no: ")
if height > 48 and ticket == "yes":
    print("Cleared to ride.")
elif height == 48:
    print("Exactly 48. Ask staff.")
else:
    print("Not cleared to ride.")'''

# ------------------------------------------------------------------ session 3, the ride log

START3 = 'heights = [52, 47, 61, 44, 58, 49, 39, 55]'
P3 = START3 + '''
cleared = 0
tallest = 0
shortest = heights[0]
for h in heights:
    if h > 48:
        cleared = cleared + 1
    if h > tallest:
        tallest = h
    if h < shortest:
        shortest = h
print(f"{cleared} of {len(heights)} riders cleared.")
print(f"Tallest {tallest}, shortest {shortest}.")
print(f"max says {max(heights)} and min says {min(heights)}")
print(f"len says {len(heights)} and sum says {sum(heights)}")'''

# ------------------------------------------------------------------ session 4, first to three

START4 = '''import random

moves = ["rock", "paper", "scissors"]
your_wins = 0
computer_wins = 0

for round_number in range(1, 4):
    print(f"Round {round_number}")
    computer = random.choice(moves)
    you = ""
    while you != "rock" and you != "paper" and you != "scissors":
        you = input("rock, paper, or scissors: ")
    print(f"You picked {you}. The computer picked {computer}.")
    if you == computer:
        print("Tie.")
    elif you == "rock" and computer == "scissors":
        print("You win.")
        your_wins = your_wins + 1
    elif you == "paper" and computer == "rock":
        print("You win.")
        your_wins = your_wins + 1
    elif you == "scissors" and computer == "paper":
        print("You win.")
        your_wins = your_wins + 1
    else:
        print("The computer wins.")
        computer_wins = computer_wins + 1
    print(f"Score: you {your_wins}, computer {computer_wins}")

print(f"Final score: you {your_wins}, computer {computer_wins}")
if your_wins > computer_wins:
    print("You win the match.")
elif your_wins == computer_wins:
    print("The match is a tie.")
else:
    print("The computer wins the match.")'''

P4 = START4
P4 = swap(P4, 'computer_wins = 0\n\nfor round_number in range(1, 4):\n    print(f"Round {round_number}")\n',
          'computer_wins = 0\nties = 0\nround_number = 0\n\nwhile your_wins < 3 and computer_wins < 3:\n    round_number = round_number + 1\n    print(f"Round {round_number}")\n')
P4 = swap(P4, '        print("Tie.")\n', '        print("Tie.")\n        ties = ties + 1\n')
P4 = swap(P4, '    print(f"Score: you {your_wins}, computer {computer_wins}")\n',
          '    print(f"Score: you {your_wins}, computer {computer_wins}, ties {ties}")\n')
P4 = swap(P4, 'print(f"Final score: you {your_wins}, computer {computer_wins}")\nif your_wins > computer_wins:\n    print("You win the match.")\nelif your_wins == computer_wins:\n    print("The match is a tie.")\nelse:',
          'print(f"Final score: you {your_wins}, computer {computer_wins}, ties {ties}")\nprint(f"Rounds played: {round_number}")\nif your_wins > computer_wins:\n    print("You win the match.")\nelse:')

# ------------------------------------------------------------------ session 6, a Mondrian from a plan

GREEN_LINE = 'GREEN = (22, 163, 74)\n'
TOP6 = swap(s6.SETUP, 'YELLOW = (252, 211, 77)\n', 'YELLOW = (252, 211, 77)\n\n' + s6.TILE_DEF + '\n')
START6 = TOP6 + '\n# ---- your drawing, done once ----\n' + s6.LOOP
CALLS6 = '''tile(YELLOW, 0, 0, 200, 200)
tile(WHITE, 200, 0, 440, 200)
tile(WHITE, 0, 200, 200, 280)
tile(RED, 200, 200, 300, 280)
tile(GREEN, 500, 200, 140, 120)
tile(BLUE, 500, 320, 140, 160)
print(f"right edges: {200 + 440} and {500 + 140}")
print(f"bottom edges: {200 + 280} and {320 + 160}")'''
P6 = swap(TOP6, 'YELLOW = (252, 211, 77)\n', 'YELLOW = (252, 211, 77)\n' + GREEN_LINE) \
    + '\n# ---- your drawing, done once ----\n' + CALLS6 + '\n' + s6.LOOP

# ------------------------------------------------------------------ session 7, the poster

START7 = '''import math
import pygame

WIDTH = 640
HEIGHT = 480
BG = (27, 41, 81)
RED = (220, 38, 38)
YELLOW = (252, 211, 77)
CREAM = (248, 250, 252)

def step_end(x, y, heading, length):
    end_x = x + length * math.cos(math.radians(heading))
    end_y = y + length * math.sin(math.radians(heading))
    return end_x, end_y

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(BG)

# ---- your drawing, done once ----

# ---- the window loop: hold the picture on screen until the window closes ----
running = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
    screen.blit(canvas, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()'''

P7 = swap(START7, '    return end_x, end_y\n', '''    return end_x, end_y

def polygon(canvas, color, x, y, heading, sides, length):
    turn = 360 / sides
    for i in range(sides):
        end_x, end_y = step_end(x, y, heading, length)
        pygame.draw.line(canvas, color, (x, y), (end_x, end_y), 3)
        x = end_x
        y = end_y
        heading = heading + turn
    return x, y, heading
''')
P7 = swap(P7, '# ---- your drawing, done once ----\n', '''# ---- your drawing, done once ----
colors = [RED, YELLOW, CREAM]
polygon(canvas, colors[0 % 3], 60, 40, 0, 3, 90)
polygon(canvas, colors[1 % 3], 500, 40, 0, 4, 80)
polygon(canvas, colors[2 % 3], 70, 330, 0, 5, 60)
polygon(canvas, colors[3 % 3], 515, 330, 0, 6, 50)
for i in range(8):
    x, y, heading = polygon(canvas, colors[i % 3], 320, 240, i * 45, 6, 40)
print(f"The last hexagon finished at ({round(x, 1)}, {round(y, 1)}).")
''')

# ------------------------------------------------------------------ session 9, names on the game

P9 = s9.C9
P9 = swap(P9, 'marks = ["X", "O"]\n', 'marks = ["X", "O"]\nname_x = input("Who plays X? ")\nname_o = input("Who plays O? ")\nnames = [name_x, name_o]\n')
P9 = swap(P9, '    player = marks[turns % 2]\n    move = input(f"Player {player}, pick a square: ")\n',
          '    player = marks[turns % 2]\n    name = names[turns % 2]\n    move = input(f"{name} ({player}), pick a square: ")\n')
P9 = swap(P9, 'if winner(board) == "":\n    print("Nobody wins. It is a draw.")\nelse:\n    print(f"{winner(board)} wins!")',
          'if winner(board) == "":\n    print("Nobody wins. It is a draw.")\nelif winner(board) == "X":\n    print(f"{names[0]} wins!")\nelse:\n    print(f"{names[1]} wins!")')

# ------------------------------------------------------------------ session 10, the message analyser

P10A = '''def tally(text):
    counts = {}
    for ch in text:
        if ch in counts:
            counts[ch] = counts[ch] + 1
        else:
            counts[ch] = 1
    return counts

message = input("Message: ")
message = message.upper()
counts = tally(message)
for ch in counts:
    print(ch, "*" * counts[ch], counts[ch])'''

P10B = P10A + '''

best = ""
best_count = 0
for ch in counts:
    if counts[ch] > best_count:
        best = ch
        best_count = counts[ch]
print(f"Most common: '{best}', {best_count} times")

book = {
    "A": "%", "E": "#", "G": "&", "H": "=", "N": "+",
    "O": "@", "S": "$", "T": "~", "U": "^", "Y": "?",
}

def encode(text):
    out = ""
    for ch in text:
        if ch in book:
            out = out + book[ch]
        else:
            out = out + ch
    return out

print(f"Original: {message}")
print(f"Encoded:  {encode(message)}")'''

# ------------------------------------------------------------------ session 11, the bouncing cabinet

START11 = '''import pygame

# ---- main variables: every number the program depends on ----
WIDTH = 640
HEIGHT = 480
R = 20
SPEED_X = 12
SPEED_Y = 7
BG = (27, 41, 81)
BALL = (252, 211, 77)
BOX = (110, 120, 150)
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
    screen.fill(BG)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()'''

P11 = swap(START11, 'clock = pygame.time.Clock()\n', '''clock = pygame.time.Clock()

x = 320
y = 240
vx = SPEED_X
vy = SPEED_Y
frame = 0
''')
P11 = swap(P11, '            running = 0\n    screen.fill(BG)\n', '''            running = 0
    x = x + vx
    y = y + vy
    if x < R:
        vx = -vx
    if x > WIDTH - R:
        vx = -vx
    if y < R:
        vy = -vy
    if y > HEIGHT - R:
        vy = -vy
    frame = frame + 1
    if frame < 11:
        print(f"frame {frame}: x = {x}, y = {y}")
    screen.fill(BG)
    pygame.draw.rect(screen, BOX, (270, 190, 100, 100))
    pygame.draw.circle(screen, BALL, (x, y), R)
''')

# ------------------------------------------------------------------ the Friday bonus, a three-bumper table

START14 = '''import math
import pygame

WIDTH = 640
HEIGHT = 480
BALL_R = 20
BUMPER_R = 30
BIG_R = 50

def distance(ax, ay, bx, by):
    dx = bx - ax
    dy = by - ay
    return math.sqrt(dx * dx + dy * dy)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

x = 100
y = 200
vx = 6
vy = 5

running = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
    x = x + vx
    y = y + vy
    if x < BALL_R:
        vx = -vx
    if x > WIDTH - BALL_R:
        vx = -vx
    if y < BALL_R:
        vy = -vy
    if y > HEIGHT - BALL_R:
        vy = -vy

    screen.fill((27, 41, 81))
    pygame.draw.circle(screen, (252, 211, 77), (x, y), BALL_R)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()'''

P14 = START14
P14 = swap(P14, '    return math.sqrt(dx * dx + dy * dy)\n', '''    return math.sqrt(dx * dx + dy * dy)

def hits(bx, by, px, py, radius):
    return distance(bx, by, px, py) < BALL_R + radius
''')
P14 = swap(P14, 'vy = 5\n', 'vy = 5\nscore = 0\nwas_touching = 0\n')
P14 = swap(P14, '        vy = -vy\n\n    screen.fill', '''        vy = -vy

    touching = 0
    points = 0
    if hits(x, y, 160, 300, BUMPER_R):
        touching = 1
        points = 100
    if hits(x, y, 480, 150, BUMPER_R):
        touching = 1
        points = 100
    if hits(x, y, 320, 240, BIG_R):
        touching = 1
        points = 50
    if touching == 1 and was_touching == 0:
        vx = -vx
        vy = -vy
        score = score + points
        print(f"hit worth {points}, score {score}")
    was_touching = touching

    screen.fill''')
P14 = swap(P14, '    screen.fill((27, 41, 81))\n', '''    screen.fill((27, 41, 81))
    pygame.draw.circle(screen, (220, 38, 38), (160, 300), BUMPER_R)
    pygame.draw.circle(screen, (220, 38, 38), (480, 150), BUMPER_R)
    pygame.draw.circle(screen, (37, 99, 235), (320, 240), BIG_R)
''')
P14 = swap(P14, '\npygame.quit()', '\nprint(f"final score {score}")\npygame.quit()')

# ------------------------------------------------------------------ the extra page, the cipher wheel

P15 = '''rack = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def shift(text, key):
    out = ""
    for ch in text:
        slot = rack.find(ch)
        if slot < 0:
            out = out + ch
        else:
            out = out + rack[(slot + key) % 26]
    return out

message = input("Message: ")
message = message.upper()
key = input("Key: ")
key = int(key)
secret = shift(message, key)
print(f"Secret:  {secret}")
print(f"Decoded: {shift(secret, -key)}")
for k in range(1, 26):
    print(k, shift("AOL JVPUZ HYL BUKLY AOL ZAHPYZ", -k))'''

RUNS = {
    1: [dict(code=P1, run="py", stdin="Ada\n52\n3\n")],
    2: [dict(code=P2, run="py", stdin="48\nmaybe\nyes\n")],
    3: [dict(code=P3, run="py")],
    4: [dict(code=P4, run="py", stdin="rock\npaper\nscissors\n" * 12, seed=35)],
    6: [dict(code=P6, run="headless", frames=3)],
    7: [dict(code=P7, run="headless", frames=3)],
    9: [dict(code=P9, run="py", stdin="Ada\nGrace\n5\n1\n4\n2\n6\n")],
    10: [dict(code=P10A, run="py", stdin="see you at the gate at ten\n"),
         dict(code=P10B, run="py", stdin="see you at the gate at ten\n")],
    11: [dict(code=P11, run="headless", frames=60)],
    15: [dict(code=P14, run="headless", frames=400)],
    16: [dict(code=P15, run="py", stdin="meet at noon\n3\n")],
}


# =================================================================== the tools

def tool(title, intro, program, steps, predict, reveal, start=None, **run):
    """One build tool: its program, its questions, and how the program is run."""
    out = {"title": title, "intro": intro + " " + HOW, "code": program, "steps": steps,
           "predict": predict, "reveal": reveal, "whole": "Show the whole program"}
    if start:
        out["start"] = start
    out.update(run)
    return out


T1 = tool(
    "The rider card, one line at a time",
    "The whole program is eight lines. Start with an empty file.",
    P1,
    [
        Q(P1, "The person at the gate asks for the rider's name. Which line asks, and stores the answer?",
          'name = input("Rider name: ")',
          'name = ____("Rider name: ")', 'input',
          ('print', "<code>print</code> puts text on the screen. It does not wait for the rider to type."),
          ('int', "<code>int</code> changes text to a whole number. A name is not a number, so Python gives an error."),
          "<code>input</code> shows the question, waits for the rider to type, and gives the typed text to the program. The text is stored under the name <code>name</code>."),
        Q(P1, "Next the height in inches. It is typed, so it arrives as text. Which two lines ask for it and change its type to a number?",
          'height = input("Height in inches: ")\nheight = int(height)',
          'height = input("Height in inches: ")\nheight = ____(height)', 'int',
          ('input', "<code>input</code> asks another question. It does not change text to a number."),
          ('print', "<code>print</code> shows a value on the screen and gives nothing back, so <code>height</code> would hold nothing."),
          "<code>input</code> always gives text, even when the rider types 52. <code>int</code> changes the type to a whole number, on a line of its own, and the number is stored back under <code>height</code>."),
        Q(P1, "The same for the tickets. Which two lines?",
          'tickets = input("How many tickets: ")\ntickets = int(tickets)',
          'tickets = ____("How many tickets: ")\ntickets = ____(tickets)', ('input', 'int'),
          (('int', 'input'), "Those are the wrong way round. The question has to be asked before the answer can be changed to a number."),
          (('input', 'input'), "The second line would ask a new question. The tickets would still be text."),
          "The same two steps as the height: ask with <code>input</code>, then change the type with <code>int</code>. Now <code>tickets</code> is a number, so the program can add to it."),
        Q(P1, "The gate says it all back in one sentence. Which line prints the name, the height, and the tickets?",
          'print(f"{name} is {height} inches tall and has {tickets} tickets.")',
          'print(f"{name} is {____} inches tall and has {tickets} tickets.")', 'height',
          ('inches', "There is no variable called <code>inches</code>. Python gives an error."),
          ('name', "That would print the name twice and leave out the height."),
          "In an f-string, each pair of braces is replaced by the value stored under the name inside it. This one sentence shows all three values the rider typed."),
        Q(P1, "The rider is given one more ticket. Which line adds 1 to the count?",
          'tickets = tickets + 1',
          'tickets = tickets ____ 1', '+',
          ('-', "That takes a ticket away."),
          ('=', "That would set <code>tickets</code> to 1, whatever the rider typed."),
          "The right side is worked out first: the old number of tickets plus 1. Then the answer is stored back under <code>tickets</code>. This works because <code>tickets</code> is a number. If it were still text, Python would give an error."),
        Q(P1, "Which line prints the new total?",
          'print(f"With one more, {name} has {tickets} tickets.")',
          'print(f"With one more, {name} has {____} tickets.")', 'tickets',
          ('tickets + 1', "<code>tickets</code> already went up by 1 on the line above. Adding 1 again would count two extra tickets."),
          ('height', "That would print the height where the tickets go."),
          "<code>tickets</code> now holds the new total, so the second sentence shows one more ticket than the rider typed."),
    ],
    "The rider types Ada, 52, and 3. What number of tickets does the last line print?",
    "4. The rider typed 3, line 5 changed that text to the number 3, and line 7 added 1. The first sentence still says 3, because it was printed before the adding.",
    run="py", stdin="Ada\n52\n3\n")

T2 = tool(
    "The ride operator, one line at a time",
    "The whole program is eleven lines. Start with an empty file.",
    P2,
    [
        Q(P2, "The operator asks for the rider's height and needs it as a number. Which two lines?",
          'height = input("Height in inches: ")\nheight = int(height)',
          'height = input("Height in inches: ")\nheight = ____(height)', 'int',
          ('input', "<code>input</code> would ask a second question. It does not change text to a number."),
          ('print', "<code>print</code> shows a value. It does not change text to a number."),
          "The gate compares the height with 48, and a comparison with a number needs a number. <code>int</code> changes the typed text to a whole number."),
        Q(P2, "The ticket question will be asked in a loop. The loop tests <code>ticket</code> before the rider has typed anything. What does <code>ticket</code> start as?",
          'ticket = ""',
          'ticket = ____', '""',
          ('"yes"', "Then the loop would not run at all, and the rider would never be asked."),
          ('0', "That would run, but <code>ticket</code> holds text everywhere else in the program, so it starts as text."),
          "Empty text is not yes and not no, so the loop asks at least once."),
        Q(P2, "The question is asked again until the answer is yes or no. Which line starts that loop?",
          'while ticket != "yes" and ticket != "no":',
          'while ticket != "yes" ____ ticket != "no":', 'and',
          ('or', "With <code>or</code> the condition is always True, because no answer is yes and no at the same time. The loop would never stop."),
          ('==', "<code>==</code> compares two values. It does not join two comparisons."),
          "The loop keeps asking while the answer is not yes and is also not no. When the rider types either word, one of the two comparisons becomes False and the loop stops."),
        Q(P2, "What goes inside the loop?",
          '    ticket = input("Do you have a ticket? Type yes or no: ")',
          '    ticket = ____("Do you have a ticket? Type yes or no: ")', 'input',
          ('print', "<code>print</code> would show the question again and again and never get an answer."),
          ('int', "The answer is a word, yes or no. <code>int</code> cannot change a word to a number."),
          "The line is indented one level, so it is inside the loop. Each time the answer is not yes or no, the question is asked again and the new answer is stored under <code>ticket</code>."),
        Q(P2, "The ride opens only for a rider taller than 48 inches who has a ticket. Which test says both, and what prints?",
          'if height > 48 and ticket == "yes":\n    print("Cleared to ride.")',
          'if height ____ 48 and ticket == ____:\n    print("Cleared to ride.")', ('>', '"yes"'),
          (('<', '"yes"'), "That opens the ride only for riders shorter than 48 inches."),
          (('>', '"no"'), "That opens the ride only for riders without a ticket."),
          "The ride opens only when both things are true: the rider is taller than 48 inches, and the ticket answer is yes. <code>and</code> is True only when both comparisons are True."),
        Q(P2, "A rider who is exactly 48 inches is sent to staff. Which two lines add that to the gate?",
          'elif height == 48:\n    print("Exactly 48. Ask staff.")',
          'elif height ____ 48:\n    print("Exactly 48. Ask staff.")', '==',
          ('=', "One equals sign stores a value. It cannot be used as a test."),
          ('>', "Then a rider taller than 48 with no ticket would be sent to staff."),
          "<code>elif</code> is a second way through the gate. Python tries it only when the first test was False. <code>==</code> asks whether the height is exactly 48."),
        Q(P2, "What about every other rider?",
          'else:\n    print("Not cleared to ride.")',
          '____:\n    print("Not cleared to ride.")', 'else',
          ('elif', "<code>elif</code> needs a test after it. This branch has no test."),
          ('while', "<code>while</code> starts a loop. This is the last branch of the gate."),
          "<code>else</code> takes every rider the two tests above did not take: a rider under 48 inches, or a rider over 48 with no ticket."),
    ],
    "The rider types 48, then maybe, then yes. How many times is the ticket question asked, and which of the three sentences prints?",
    "Twice. maybe is not yes or no, so the loop asks again. Then the height is not more than 48, so the first test is False. The <code>elif</code> is True, because the height is exactly 48, and the program prints Exactly 48. Ask staff.",
    run="py", stdin="48\nmaybe\nyes\n")

T3 = tool(
    "The ride log, one line at a time",
    "The list of eight heights is given. Copy it from the button below, then write the lines under it.",
    P3,
    [
        Q(P3, "The log counts how many riders cleared 48 inches. What does the counter start as?",
          'cleared = 0',
          'cleared = ____', '0',
          ('1', "No height has been checked yet."),
          ('heights', "<code>heights</code> is the list. A counter is a number."),
          "A counter starts at 0 because nothing has been counted yet. The line is above the loop, so it runs once."),
        Q(P3, "Best so far is used twice: once for the tallest and once for the shortest. What do the two names start as?",
          'tallest = 0\nshortest = heights[0]',
          'tallest = 0\nshortest = ____', 'heights[0]',
          ('0', "No height is smaller than 0, so <code>shortest</code> would stay 0 and never change."),
          ('heights', "That is the whole list, not one height. A height cannot be compared with a list."),
          "<code>tallest</code> can start at 0 because every height beats it. <code>shortest</code> needs a start that a height can be smaller than, so it starts as the first height in the list. If a shorter one comes along, it takes over."),
        Q(P3, "Which line visits every height in the list?",
          'for h in heights:',
          'for h in ____:', 'heights',
          ('range(8)', "Then <code>h</code> would hold 0, 1, 2, and so on up to 7, not the heights."),
          ('len(heights)', "<code>len(heights)</code> is one number, 8. A loop cannot go over a single number."),
          "A <code>for</code> loop over a list puts one item in the loop variable on each pass. <code>h</code> holds 52 first, then 47, and so on to the end."),
        Q(P3, "A rider clears when the height is more than 48. Which gate counts those riders?",
          '    if h > 48:\n        cleared = cleared + 1',
          '    if h ____ 48:\n        cleared = cleared ____ 1', ('>', '+'),
          (('<', '+'), "That counts the riders who are too short."),
          (('>', '-'), "That takes 1 away for every rider who clears."),
          "The gate opens only for a height over 48. Then the counter goes up by 1. Heights that do not clear leave the counter alone."),
        Q(P3, "Which gate keeps the tallest height so far?",
          '    if h > tallest:\n        tallest = h',
          '    if h > ____:\n        tallest = ____', ('tallest', 'h'),
          (('48', 'h'), "That keeps the last height over 48, not the tallest one."),
          (('tallest', 'tallest'), "That stores the value <code>tallest</code> already has, so it never changes."),
          "When this height is bigger than the best so far, it becomes the new best so far. After the last pass, <code>tallest</code> holds the biggest height in the list."),
        Q(P3, "Which gate keeps the shortest height so far?",
          '    if h < shortest:\n        shortest = h',
          '    if h ____ shortest:\n        shortest = h', '<',
          ('>', "That finds the tallest again."),
          ('==', "That is True only when <code>h</code> is the same as <code>shortest</code>, and then nothing changes."),
          "<code>h &lt; shortest</code> is True when this height is smaller than the smallest so far. Then it becomes the new shortest."),
        Q(P3, "After the loop, two lines give the summary. What goes in the first pair of braces?",
          'print(f"{cleared} of {len(heights)} riders cleared.")\nprint(f"Tallest {tallest}, shortest {shortest}.")',
          'print(f"{____} of {len(heights)} riders cleared.")\nprint(f"Tallest {tallest}, shortest {shortest}.")', 'cleared',
          ('h', "<code>h</code> holds the last height in the list, which is 55."),
          ('heights', "That prints the whole list."),
          "The two lines are at the left edge, so they run once, after the loop. The braces are replaced by the count, the number of riders, the tallest, and the shortest."),
        Q(P3, "Python has built-in tools that find the same answers. Which two lines check your work?",
          'print(f"max says {max(heights)} and min says {min(heights)}")\nprint(f"len says {len(heights)} and sum says {sum(heights)}")',
          'print(f"max says {____(heights)} and min says {min(heights)}")\nprint(f"len says {len(heights)} and sum says {sum(heights)}")', 'max',
          ('tallest', "<code>tallest</code> is a number, not a function. It cannot be called with parentheses."),
          ('sum', "<code>sum</code> adds the heights up. It does not find the biggest."),
          "<code>max</code> and <code>min</code> are built in. If they print the same numbers as your <code>tallest</code> and <code>shortest</code>, your loop is right. No built-in counts how many heights are over 48, so that one you had to write."),
    ],
    "Before you run it: how many of the eight heights are over 48, and which height is the shortest?",
    "Five are over 48: 52, 61, 58, 49, and 55. The shortest is 39. <code>max</code> and <code>min</code> print 61 and 39, the same as the hand-written loop.",
    start=START3, run="py")

T4 = tool(
    "First to three, one line at a time",
    "Start from the chunk 8 program, which is behind the button below. The line numbers in the questions are the line numbers in the finished program.",
    P4,
    [
        Q(P4, "The game needs two more counters above the loop: one for ties, and one for rounds, because <code>range</code> will no longer count them. What do they start as?",
          'ties = 0\nround_number = 0',
          'ties = ____\nround_number = ____', ('0', '0'),
          (('1', '1'), "No round has been played and no tie has happened yet."),
          (('0', '1'), "The loop adds 1 before it prints the round, so the first round would be called Round 2."),
          "Both are counters, and nothing has been counted yet.",
          note="Under <code>computer_wins = 0</code>."),
        Q(P4, "The game lasts until someone has won three rounds. Which line takes the place of the <code>for</code> line?",
          'while your_wins < 3 and computer_wins < 3:',
          'while your_wins < 3 ____ computer_wins < 3:', 'and',
          ('or', "With <code>or</code> the game would keep going until both players have 3 wins."),
          ('==', "<code>==</code> compares two values. It does not join two comparisons."),
          "The game goes on while neither player has reached 3. As soon as one counter is 3, its comparison is False, and <code>and</code> makes the whole condition False.",
          note="The lines under it stay exactly as they are."),
        Q(P4, "Which line counts the round, and where does it go?",
          '    round_number = round_number + 1',
          '    round_number = round_number ____ 1', '+',
          ('-', "The rounds would be numbered -1, -2, -3."),
          ('*', "0 times 1 is 0, so every round would be Round 0."),
          "It is the first line inside the loop, above the line that prints the round. The first pass makes it 1, so the first round prints as Round 1."),
        Q(P4, "A tie has to be counted too. Which line, and in which branch?",
          '        ties = ties + 1',
          '        ____ = ties + 1', 'ties',
          ('your_wins', "A tie would count as a win for the player."),
          ('tie', "That makes a new variable called <code>tie</code>. <code>ties</code> would stay at 0."),
          "The line goes under <code>print(\"Tie.\")</code>, two indentation levels in, so it runs only in a tied round."),
        Q(P4, "The score line shows two counters. How does it show all three?",
          '    print(f"Score: you {your_wins}, computer {computer_wins}, ties {ties}")',
          '    print(f"Score: you {your_wins}, computer {computer_wins}, ties {____}")', 'ties',
          ('round_number', "That would print the round number under the word ties."),
          ('your_wins', "That would print the player's wins twice."),
          "One more pair of braces in the f-string, with the third counter inside it."),
        Q(P4, "After the loop, the final score shows all three counters, and a second line says how many rounds were played. What goes in its braces?",
          'print(f"Final score: you {your_wins}, computer {computer_wins}, ties {ties}")\nprint(f"Rounds played: {round_number}")',
          'print(f"Final score: you {your_wins}, computer {computer_wins}, ties {ties}")\nprint(f"Rounds played: {____}")', 'round_number',
          ('3', "The match can take more than 3 rounds."),
          ('ties', "That is the number of tied rounds, not all the rounds."),
          "<code>round_number</code> went up by 1 on every pass of the loop, so after the loop it holds the number of rounds played."),
        Q(P4, "The match can end only two ways now. What does the gate look like with two branches?",
          'if your_wins > computer_wins:\n    print("You win the match.")\nelse:\n    print("The computer wins the match.")',
          'if your_wins > computer_wins:\n    print("You win the match.")\n____:\n    print("The computer wins the match.")', 'else',
          ('elif your_wins == computer_wins', "The loop stops only when one counter is 3 and the other is less, so the two counters are never equal here."),
          ('elif', "<code>elif</code> needs a test after it."),
          "The loop ends only when one player has 3 wins and the other has fewer. The counters cannot be equal, so the tie branch is gone and two branches are enough."),
    ],
    "Look at the last score line of the run. Add its three numbers. What should they add up to, and why?",
    "7, the number of rounds played: 2 wins for the player, 3 for the computer, and 2 ties. Every round adds 1 to exactly one of the three counters. The game stopped in round 7, when the computer reached 3. Your run will be different, because the computer picks at random.",
    start=START4, run="py", stdin="rock\npaper\nscissors\n" * 12, seed=35)

T6 = tool(
    "A Mondrian from a plan, one call at a time",
    "Your own picture comes from your own paper plan. This tool works through one plan, so you can see how each number is found. The plan has a top row 200 tall and a bottom row 280 tall. Top row: a yellow tile 200 wide, then a white tile that goes to the right edge. Bottom row: a white tile 200 wide, then a red tile 300 wide, then a green tile above a blue tile, each 140 wide. The green tile is 120 tall. The starting file is behind the button below: the setup, the function, an empty drawing section, and the loop.",
    P6,
    [
        Q(P6, "Green is a new colour, and it needs a name next to the other colours. Which line adds it?",
          'GREEN = (22, 163, 74)',
          '____ = (22, 163, 74)', 'GREEN',
          ('green', "The other colour names are in capitals, and this one should match them."),
          ('"GREEN"', "A name has no quote marks. Python gives an error."),
          "A colour is three numbers from 0 to 255: red, green, and blue. Giving the three numbers a capitalised name means a call can say <code>GREEN</code>.",
          note="Under the <code>YELLOW</code> line."),
        Q(P6, "The yellow tile is in the top left corner of the window. Where does it start?",
          'tile(YELLOW, 0, 0, 200, 200)',
          'tile(YELLOW, ____, ____, 200, 200)', ('0', '0'),
          (('200', '200'), "That is where the yellow tile ends, not where it starts."),
          (('640', '480'), "That is the bottom right corner of the window. The tile would be drawn off the screen."),
          "The top left corner of the window is x = 0, y = 0. The tile is 200 wide and 200 tall, so it ends at x = 200 and y = 200.",
          note="Under the comment <code># ---- your drawing, done once ----</code>."),
        Q(P6, "The white tile beside it fills the rest of the top row. Where does it start, and how wide is it?",
          'tile(WHITE, 200, 0, 440, 200)',
          'tile(WHITE, ____, 0, ____, 200)', ('200', '440'),
          (('200', '640'), "640 is the width of the whole window. The tile starts at 200, so only 440 is left."),
          (('0', '440'), "That starts on top of the yellow tile."),
          "It starts where the yellow tile ends, at x = 200. The window is 640 wide, and 640 take away 200 leaves 440."),
        Q(P6, "The bottom row starts under the yellow tile and goes to the bottom of the window. Where does the first white tile start, and how tall is it?",
          'tile(WHITE, 0, 200, 200, 280)',
          'tile(WHITE, 0, ____, 200, ____)', ('200', '280'),
          (('200', '480'), "480 is the height of the whole window. The tile starts at 200, so only 280 is left."),
          (('0', '280'), "That starts on top of the yellow tile."),
          "The top row ends at y = 200, so the bottom row starts there. The window is 480 tall, and 480 take away 200 leaves 280."),
        Q(P6, "The red tile is next to that white tile, in the bottom row. Where does it start?",
          'tile(RED, 200, 200, 300, 280)',
          'tile(RED, ____, ____, 300, 280)', ('200', '200'),
          (('0', '200'), "That starts on top of the white tile."),
          (('200', '0'), "That is in the top row, on top of the white tile there."),
          "The white tile beside it ends at x = 200, and the bottom row starts at y = 200. Tiles that touch share a number."),
        Q(P6, "The green tile is to the right of the red one. Where does it start, and how wide is it?",
          'tile(GREEN, 500, 200, 140, 120)',
          'tile(GREEN, ____, 200, ____, 120)', ('500', '140'),
          (('300', '140'), "300 is the red tile's width. The red tile starts at 200, so it ends at 500."),
          (('500', '640'), "640 is the width of the whole window. From 500 to the right edge is 140."),
          "The red tile starts at 200 and is 300 wide, so it ends at 500. From 500 to the right edge at 640 is 140."),
        Q(P6, "The blue tile is under the green one and goes to the bottom. Where does it start, and how tall is it?",
          'tile(BLUE, 500, 320, 140, 160)',
          'tile(BLUE, 500, ____, 140, ____)', ('320', '160'),
          (('200', '160'), "That starts on top of the green tile."),
          (('320', '480'), "480 is the height of the whole window. From 320 to the bottom is 160."),
          "The green tile starts at y = 200 and is 120 tall, so it ends at 320. From 320 to the bottom at 480 is 160."),
        Q(P6, "Before trusting the picture, let Python check the edges. A tile's right edge is its x plus its width. What goes in the blank?",
          'print(f"right edges: {200 + 440} and {500 + 140}")\nprint(f"bottom edges: {200 + 280} and {320 + 160}")',
          'print(f"right edges: {200 + 440} and {500 + ____}")\nprint(f"bottom edges: {200 + 280} and {320 + 160}")', '140',
          ('500', "500 is where the tile starts. Its width is 140."),
          ('640', "640 is where the edge should be. The sum has to use the tile's own width, or it checks nothing."),
          "Each sum is a tile's start plus its size. If the plan has no gaps, both right edges come to 640 and both bottom edges come to 480."),
    ],
    "Two right edges and two bottom edges are printed. What should the four numbers be if no tile stops short of the edge of the window?",
    "640 and 640, then 480 and 480. The window is 640 wide and 480 tall, and each sum is the far edge of a tile that touches the right side or the bottom. On your own plan, write these sums for your own edge tiles.",
    start=START6, run="headless", frames=3)

T7 = tool(
    "The poster, one line at a time",
    "The starting file is behind the button below: the colours, <code>step_end</code> from chunk 2, the canvas, an empty drawing section, and the window loop from chunk 3. The function <code>polygon</code> goes under <code>step_end</code>, and the drawing goes under the drawing comment.",
    P7,
    [
        Q(P7, "<code>polygon</code> draws a closed shape with any number of sides. Its first line works out how far the pen turns at each corner. What is the turn?",
          'def polygon(canvas, color, x, y, heading, sides, length):\n    turn = 360 / sides',
          'def polygon(canvas, color, x, y, heading, sides, length):\n    turn = ____ / sides', '360',
          ('180', "A pen that comes back to where it started has turned all the way round, and all the way round is 360 degrees."),
          ('sides', "<code>sides / sides</code> is 1, so the pen would turn 1 degree at every corner."),
          "A closed shape turns through 360 degrees in total. Shared equally between the corners, each turn is 360 divided by the number of sides.",
          note="Under <code>step_end</code>, at the left edge, with an empty line above."),
        Q(P7, "How many times does the pen draw a side and turn?",
          '    for i in range(sides):',
          '    for i in range(____):', 'sides',
          ('360', "That would draw 360 sides, going round the shape many times."),
          ('turn', "<code>turn</code> can be a number with a decimal point, and <code>range</code> needs a whole number."),
          "One pass of the loop draws one side, so the loop runs once for each side."),
        Q(P7, "Each side starts at the pen and ends somewhere else. Which function works out where it ends?",
          '        end_x, end_y = step_end(x, y, heading, length)',
          '        end_x, end_y = ____(x, y, heading, length)', 'step_end',
          ('polygon', "Then <code>polygon</code> would call itself, and it would never finish."),
          ('turn', "<code>turn</code> is a number, not a function."),
          "<code>step_end</code> takes where the pen is, which way it is facing, and how far it goes. It returns two numbers, and the two names on the left take them in order."),
        Q(P7, "Which line draws the side?",
          '        pygame.draw.line(canvas, color, (x, y), (end_x, end_y), 3)',
          '        pygame.draw.line(canvas, color, (x, y), (____, ____), 3)', ('end_x', 'end_y'),
          (('x', 'y'), "A line from a point to the same point has no length, so nothing would be drawn."),
          (('end_y', 'end_x'), "Those are swapped. The x has to come first."),
          "A line goes from one point to another. It starts where the pen is, at (x, y), and ends at the point <code>step_end</code> worked out."),
        Q(P7, "The side is drawn. What three things change before the next side?",
          '        x = end_x\n        y = end_y\n        heading = heading + turn',
          '        x = end_x\n        y = end_y\n        heading = heading ____ turn', '+',
          ('*', "The first heading is 0, and 0 times any number is 0, so the pen would never turn."),
          ('=', "That would set the heading to the same number every time, so the pen would turn once and then go straight."),
          "The pen moves to the end of the side it just drew. Then its heading goes up by one turn, so the next side points in a new direction."),
        Q(P7, "After the last side, what does the function return?",
          '    return x, y, heading',
          '    return x, y, ____', 'heading',
          ('turn', "<code>turn</code> is the size of one turn. The caller wants to know which way the pen is facing at the end."),
          ('sides', "The caller already knows the number of sides. It gave that number to the function."),
          "The function returns where the pen finished and which way it is facing. For a closed shape, that is the point where it started."),
        Q(P7, "The four shapes take their colours from a list. Which line makes the list?",
          'colors = [RED, YELLOW, CREAM]',
          '____ = [RED, YELLOW, CREAM]', 'colors',
          ('color', "<code>color</code> is the name of a parameter inside <code>polygon</code>. The list needs a name of its own."),
          ('"colors"', "A name has no quote marks. Python gives an error."),
          "A list holds the three colours in order, in slots 0, 1, and 2.",
          note="Under the comment <code># ---- your drawing, done once ----</code>."),
        Q(P7, "Four shapes, one near each corner, each with a different number of sides. The colour index is the shape's number % 3. What goes in the two blanks?",
          'polygon(canvas, colors[0 % 3], 60, 40, 0, 3, 90)\npolygon(canvas, colors[1 % 3], 500, 40, 0, 4, 80)\npolygon(canvas, colors[2 % 3], 70, 330, 0, 5, 60)\npolygon(canvas, colors[3 % 3], 515, 330, 0, 6, 50)',
          'polygon(canvas, colors[0 % 3], 60, 40, 0, ____, 90)\npolygon(canvas, colors[1 % 3], 500, 40, 0, 4, 80)\npolygon(canvas, colors[2 % 3], 70, 330, 0, 5, 60)\npolygon(canvas, colors[3 % ____], 515, 330, 0, 6, 50)', ('3', '3'),
          (('3', '4'), "<code>3 % 4</code> is 3, and the list has no slot 3."),
          (('0', '3'), "A shape cannot have 0 sides. <code>360 / 0</code> gives an error."),
          "The four calls have 3, 4, 5, and 6 sides. The remainder after dividing by 3 is always 0, 1, or 2, so it is always a slot in the list. The fourth shape gets <code>3 % 3</code>, which is 0, so it uses the first colour again."),
        Q(P7, "The rosette in the middle is eight hexagons, each one turned a little more than the one before. How many copies, and how far apart?",
          'for i in range(8):\n    x, y, heading = polygon(canvas, colors[i % 3], 320, 240, i * 45, 6, 40)',
          'for i in range(____):\n    x, y, heading = polygon(canvas, colors[i % 3], 320, 240, i * ____, 6, 40)', ('8', '45'),
          (('8', '30'), "8 times 30 is 240, not 360, so the ring would have a gap in it."),
          (('45', '8'), "Those are swapped. That draws 45 hexagons, 8 degrees apart."),
          "Eight copies share a full turn of 360 degrees, so each one starts 45 degrees after the last. <code>i * 45</code> gives the headings 0, 45, 90, and so on to 315."),
        Q(P7, "The last hexagon's pen position is stored in <code>x</code> and <code>y</code>. Which line prints it?",
          'print(f"The last hexagon finished at ({round(x, 1)}, {round(y, 1)}).")',
          'print(f"The last hexagon finished at ({round(x, 1)}, {round(____, 1)}).")', 'y',
          ('heading', "<code>heading</code> is the direction the pen faces, not how far down it is."),
          ('x', "That would print the x twice."),
          "Words go in the terminal. If the shape closed, the printed point is the point where the hexagon started."),
    ],
    "Every hexagon in the rosette starts at (320, 240). Where does the last one finish?",
    "At (320.0, 240.0), the point where it started. Six sides with six turns of 60 degrees add up to 360, so the pen comes back to its start. That is the check that the shape closes.",
    start=START7, run="headless", frames=3)

T9 = tool(
    "Names on the game, one line at a time",
    "Start from the chunk 9 program, which is behind the button below. The line numbers in the questions are the line numbers in the finished program. Do the test sheet first.",
    P9,
    [
        Q(P9, "Before the game starts, the program asks who is playing. The names go in a list in the same order as the marks. What goes in the two blanks?",
          'name_x = input("Who plays X? ")\nname_o = input("Who plays O? ")\nnames = [name_x, name_o]',
          'name_x = ____("Who plays X? ")\nname_o = input("Who plays O? ")\nnames = [name_x, ____]', ('input', 'name_o'),
          (('print', 'name_o'), "<code>print</code> shows the question but does not wait for an answer."),
          (('input', 'name_x'), "Then both slots of the list would hold the name of the X player."),
          "<code>marks</code> holds X in slot 0 and O in slot 1. <code>names</code> holds the X player's name in slot 0 and the O player's name in slot 1, so one index picks the right mark and the right name.",
          note="Under the <code>marks</code> line."),
        Q(P9, "<code>marks[turns % 2]</code> picks the mark for this turn. Which line picks the name?",
          '    name = names[turns % 2]',
          '    name = names[____]', 'turns % 2',
          ('turns', "<code>turns</code> goes up to 8, and the list has only slots 0 and 1."),
          ('player', "<code>player</code> holds X or O. An index has to be a whole number."),
          "The same index picks the name. When <code>turns</code> is even it is 0, the X player. When <code>turns</code> is odd it is 1, the O player.",
          note="Under the <code>player</code> line, one indentation level in."),
        Q(P9, "The question should say the player's name and mark, like Ada (X), pick a square. What goes in the first pair of braces?",
          '    move = input(f"{name} ({player}), pick a square: ")',
          '    move = input(f"{____} ({player}), pick a square: ")', 'name',
          ('names', "That would print the whole list of both names."),
          ('name_x', "That would print the X player's name on every turn."),
          "<code>name</code> holds the name of the player whose turn it is, and <code>player</code> holds the mark. The parentheses inside the string are ordinary characters that get printed."),
        Q(P9, "<code>winner(board)</code> returns a mark, not a name. Which branch prints the X player's name?",
          'elif winner(board) == "X":\n    print(f"{names[0]} wins!")',
          'elif winner(board) == ____:\n    print(f"{names[____]} wins!")', ('"X"', '0'),
          (('"X"', '1'), "<code>names[1]</code> is the O player's name."),
          (('"O"', '0'), "That would print the X player's name when O wins."),
          "When the winner's mark is X, the winner's name is in slot 0 of <code>names</code>. It is a second way through the gate, so it starts with <code>elif</code>.",
          note="Between the draw branch and the <code>else</code>."),
        Q(P9, "The only case left is that O won. What does the last branch print?",
          'else:\n    print(f"{names[1]} wins!")',
          'else:\n    print(f"{names[____]} wins!")', '1',
          ('2', "The list has two names, in slots 0 and 1. There is no slot 2."),
          ('0', "That is the X player's name, and X did not win in this branch."),
          "The gate has three ways through: a draw, X won, and every other case. The only other case is that O won, and O's name is in slot 1."),
    ],
    "Ada plays X and Grace plays O. The moves are 5, 1, 4, 2, and 6. What is the last line the program prints?",
    "Ada wins! X has squares 4, 5, and 6, the middle row, so <code>winner(board)</code> returns X and the program prints the name in slot 0.",
    start=s9.C9, run="py", stdin="Ada\nGrace\n5\n1\n4\n2\n6\n")

T10A = tool(
    "Tool 1: tally and the star chart, one line at a time",
    "Start with an empty file. This tool is the floor of today's build.",
    P10A,
    [
        Q(P10A, "<code>tally</code> takes some text and counts each character in a dictionary. What does the dictionary start as?",
          'def tally(text):\n    counts = {}',
          'def tally(text):\n    counts = ____', '{}',
          ('[]', "<code>[]</code> is an empty list. A list has no keys, so a character cannot be looked up in it."),
          ('0', "<code>0</code> is one number. The function needs somewhere to keep a count for every character."),
          "Curly braces with nothing inside make an empty dictionary. No character has been counted yet."),
        Q(P10A, "Which line visits every character of the text?",
          '    for ch in text:',
          '    for ch in ____:', 'text',
          ('counts', "<code>counts</code> is empty at this point, so the loop would not run at all."),
          ('message', "<code>message</code> is a name outside the function. The function should work on whatever text it is given."),
          "A <code>for</code> loop over a string puts one character in <code>ch</code> on each pass, spaces included."),
        Q(P10A, "The character has been seen before. Which test finds that out, and what happens to its count?",
          '        if ch in counts:\n            counts[ch] = counts[ch] + 1',
          '        if ch ____ counts:\n            counts[ch] = counts[ch] + ____', ('in', '1'),
          (('==', '1'), "A single character is never equal to a whole dictionary."),
          (('in', 'ch'), "That adds a character to a number, and Python gives an error."),
          "<code>in</code> checks the keys of the dictionary. If the character is already a key, its count goes up by 1."),
        Q(P10A, "The character has not been seen before. What happens then?",
          '        else:\n            counts[ch] = 1',
          '        else:\n            counts[ch] = ____', '1',
          ('0', "The character has just been seen once, so its count is 1."),
          ('ch', "That stores the character itself, not a count."),
          "Storing a value under a new key adds that key to the dictionary. The first time a character is seen, its count is 1. Without the gate, asking for a key that is not there gives a KeyError."),
        Q(P10A, "The loop is done. How does the caller get the dictionary?",
          '    return counts',
          '    return ____', 'counts',
          ('text', "That returns the text the caller gave, not the counts."),
          ('ch', "<code>ch</code> holds only the last character of the text."),
          "<code>return</code> gives the dictionary to the line that called <code>tally</code>. The line is lined up with the <code>for</code>, so it runs after every character has been counted. The function returns the dictionary and does not print it."),
        Q(P10A, "The program asks for a message. A small s and a capital S should count as the same character. Which line takes care of that?",
          'message = input("Message: ")\nmessage = message.upper()',
          'message = input("Message: ")\nmessage = message.____()', 'upper',
          ('strip', "<code>strip</code> removes spaces from the two ends. It does not change the letters, so s and S would be counted as two different characters."),
          ('tally', "<code>tally</code> is a function that is called with the text in its parentheses. It is not something a string can do."),
          "<code>upper</code> returns the message with every letter as a capital, and the result is stored back under <code>message</code>.",
          note="At the left edge, under the function, with an empty line above."),
        Q(P10A, "Which line counts the characters of the message?",
          'counts = tally(message)',
          'counts = ____(message)', 'tally',
          ('len', "<code>len</code> gives how many characters the message has. It does not count each one separately."),
          ('input', "<code>input</code> would ask another question."),
          "The call gives the message to <code>tally</code> and is replaced by the dictionary it returns."),
        Q(P10A, "The star chart prints one line for each character: the character, a star for each time it appears, and the count. Which lines?",
          'for ch in counts:\n    print(ch, "*" * counts[ch], counts[ch])',
          'for ch in counts:\n    print(ch, "*" ____ counts[ch], counts[ch])', '*',
          ('+', "Text plus a number gives an error."),
          (',', "That prints one star and then the count twice."),
          "A loop over a dictionary gives its keys, one on each pass. Text times a number repeats the text, so <code>\"*\" * 5</code> is five stars."),
    ],
    "The message is see you at the gate at ten. Which character gets the most stars, and how many?",
    "The space, with 6. There are seven words, so there are six spaces between them. E and T come next with 5 each.",
    run="py", stdin="see you at the gate at ten\n")

T10B = tool(
    "Tool 2: the most common character and a codebook",
    "This tool carries on from tool 1. The program so far is behind the button below.",
    P10B,
    [
        Q(P10B, "Best so far, from session 3, finds the most common character. Two names are needed: the best character and its count. What does the count start as?",
          'best = ""\nbest_count = 0',
          'best = ""\nbest_count = ____', '0',
          ('1', "Then a character that appears once could never beat the start."),
          ('""', "A count is a number. A number cannot be compared with empty text."),
          "Every count in the dictionary is at least 1, so the first character the loop looks at beats 0 and becomes the best so far.",
          note="At the left edge, under the star chart, with an empty line above."),
        Q(P10B, "Which loop and gate keep the character with the biggest count?",
          'for ch in counts:\n    if counts[ch] > best_count:\n        best = ch\n        best_count = counts[ch]',
          'for ch in counts:\n    if counts[ch] ____ best_count:\n        best = ____\n        best_count = counts[ch]', ('>', 'ch'),
          (('<', 'ch'), "No count is less than 0, so the gate would never open."),
          (('>', 'counts'), "That stores the whole dictionary, not one character."),
          "The loop goes over the keys. When a character's count is bigger than the best so far, that character and its count take over."),
        Q(P10B, "Which line prints the most common character and its count?",
          'print(f"Most common: \'{best}\', {best_count} times")',
          'print(f"Most common: \'{best}\', {____} times")', 'best_count',
          ('counts', "That prints the whole dictionary."),
          ('best', "That prints the character twice and leaves out the count."),
          "The single quote marks are ordinary characters inside the string. They are printed on each side of the character, so a space can be seen."),
        Q(P10B, "The codebook is a dictionary with ten pairs. Each pair is a letter and the symbol that takes its place. What goes between a key and its value?",
          'book = {\n    "A": "%", "E": "#", "G": "&", "H": "=", "N": "+",\n    "O": "@", "S": "$", "T": "~", "U": "^", "Y": "?",\n}',
          'book = {\n    "A"____ "%", "E": "#", "G": "&", "H": "=", "N": "+",\n    "O": "@", "S": "$", "T": "~", "U": "^", "Y": "?",\n}', ':',
          ('=', "An equals sign stores a value under a name. Inside a dictionary, a pair is written with a colon."),
          (',', "A comma goes between two pairs, not between a key and its value."),
          "Each pair is a key, a colon, and a value, with commas between the pairs. A dictionary can be written across several lines, as long as the braces open and close around all of it."),
        Q(P10B, "<code>encode</code> builds a new string one character at a time. What does the string start as?",
          'def encode(text):\n    out = ""',
          'def encode(text):\n    out = ____', '""',
          ('{}', "<code>{}</code> is an empty dictionary. The answer is a string."),
          ('text', "Then the answer would start with the whole message, before any character was encoded."),
          "<code>out</code> is built by adding one character at a time, so it starts as empty text.",
          note="At the left edge, under the codebook, with an empty line above."),
        Q(P10B, "The character is in the codebook. What is added to <code>out</code>?",
          '    for ch in text:\n        if ch in book:\n            out = out + book[ch]',
          '    for ch in text:\n        if ch in book:\n            out = out + ____', 'book[ch]',
          ('ch', "That adds the letter itself, so nothing would be encoded."),
          ('book', "Text plus a whole dictionary gives an error."),
          "<code>book[ch]</code> looks the letter up and gives its symbol. The gate makes sure the letter is a key before the lookup."),
        Q(P10B, "The character is not in the codebook. What is added then, and what does the function return?",
          '        else:\n            out = out + ch\n    return out',
          '        else:\n            out = out + ____\n    return out', 'ch',
          ('""', "Empty text adds nothing, so spaces and every other character would disappear."),
          ('book[ch]', "In this branch the character is not a key of the codebook, so the lookup gives a KeyError."),
          "A character with no pair in the codebook is added as it is, so spaces and any letter outside the ten come through unchanged."),
        Q(P10B, "The last two lines print the message and the encoded message with labels. Which function goes in the second one?",
          'print(f"Original: {message}")\nprint(f"Encoded:  {encode(message)}")',
          'print(f"Original: {message}")\nprint(f"Encoded:  {____(message)}")', 'encode',
          ('tally', "<code>tally</code> returns the dictionary of counts, not an encoded message."),
          ('book', "<code>book</code> is a dictionary, not a function. It cannot be called with parentheses."),
          "The call is replaced by the string <code>encode</code> returns. The two labels are the same length, so the two messages line up one above the other."),
    ],
    "Which characters of the message come through the codebook unchanged?",
    "Only the spaces. Every letter in SEE YOU AT THE GATE AT TEN is one of the ten keys of the codebook, so every letter is replaced by its symbol. The spaces are not keys, so the <code>else</code> adds them as they are.",
    start=P10A, run="py", stdin="see you at the gate at ten\n")

T11 = tool(
    "The bouncing cabinet, one line at a time",
    "The starting file is behind the button below: the main variables, and the frame loop from chunk 2. Run it and check that an empty window opens. Then add the lines.",
    P11,
    [
        Q(P11, "The ball starts in the middle of the window. The window is 640 wide and 480 tall. What are the two lines?",
          'x = 320\ny = 240',
          'x = ____\ny = ____', ('320', '240'),
          (('640', '480'), "That is the bottom right corner of the window."),
          (('0', '0'), "That is the top left corner, so most of the ball would be outside the window."),
          "<code>x</code> and <code>y</code> are the centre of the ball. Half of 640 is 320 and half of 480 is 240.",
          note="Under the <code>clock</code> line, with an empty line above."),
        Q(P11, "Velocity is two numbers: how far the ball moves across and how far it moves down on each frame. Where do the starting values come from?",
          'vx = SPEED_X\nvy = SPEED_Y',
          'vx = ____\nvy = ____', ('SPEED_X', 'SPEED_Y'),
          (('12', '7'), "That works today, but with raw numbers here, changing the main variables would do nothing."),
          (('SPEED_Y', 'SPEED_X'), "Those are swapped. <code>vx</code> is the speed across."),
          "The speeds are main variables. Using the names means the speed can be changed in one place, at the top of the file."),
        Q(P11, "On every frame the ball moves. Which two lines move it?",
          '    x = x + vx\n    y = y + vy',
          '    x = x ____ vx\n    y = y + ____', ('+', 'vy'),
          (('+', 'vx'), "Then <code>y</code> would change by the speed across, and <code>vy</code> would never be used."),
          (('*', 'vy'), "Multiplying makes <code>x</code> many times bigger on every frame. The ball would leave the window at once."),
          "The new position is the old position plus the velocity. The lines are inside the frame loop, so the ball moves a little on every frame.",
          note="Inside the loop, under the <code>for event</code> loop and above <code>screen.fill(BG)</code>."),
        Q(P11, "The ball reaches the left wall. Which gate turns it round?",
          '    if x < R:\n        vx = -vx',
          '    if x < ____:\n        vx = ____', ('R', '-vx'),
          (('0', '-vx'), "<code>x</code> is the centre of the ball. By the time the centre reaches 0, half the ball is through the wall."),
          (('R', '0'), "That stops the ball moving across. It would slide straight up or down the wall."),
          "The edge of the ball touches the wall when its centre is one radius away from it. <code>-vx</code> is the same speed in the other direction, so the ball turns round."),
        Q(P11, "And the right wall?",
          '    if x > WIDTH - R:\n        vx = -vx',
          '    if x > ____:\n        vx = -vx', 'WIDTH - R',
          ('WIDTH', "The centre would reach the wall before the ball turned, so half the ball would leave the window."),
          ('R', "That is True almost everywhere in the window, so the ball would turn round on nearly every frame."),
          "The right wall is at <code>WIDTH</code>. The ball's edge touches it when the centre is one radius short of it."),
        Q(P11, "The top and the bottom work the same way, with <code>y</code> and <code>vy</code>. What goes in the two blanks?",
          '    if y < R:\n        vy = -vy\n    if y > HEIGHT - R:\n        vy = -vy',
          '    if y < R:\n        vy = -vy\n    if y > ____ - R:\n        vy = ____', ('HEIGHT', '-vy'),
          (('WIDTH', '-vy'), "<code>WIDTH</code> is how far across the window goes. The bottom wall is at <code>HEIGHT</code>."),
          (('HEIGHT', '-vx'), "That stores the speed across in the speed down."),
          "Four flat gates, one for each wall. The top and bottom gates change <code>vy</code>, because those walls stop the ball moving up or down."),
        Q(P11, "A probe prints the position for the first ten frames. First the frames have to be counted. Where does the counter start, and what happens to it on every frame?",
          'frame = 0', 'frame = ____\n    frame = frame + ____', ('0', '1'),
          (('1', '1'), "Then the first frame would be counted as frame 2."),
          (('0', '0'), "Adding 0 changes nothing, so the counter would stay at 0."),
          "The counter starts at 0 above the loop and goes up by 1 on every frame, inside the loop, after the four gates.",
          part2='    frame = frame + 1'),
        Q(P11, "Which gate lets the probe print on frames 1 to 10 only?",
          '    if frame < 11:\n        print(f"frame {frame}: x = {x}, y = {y}")',
          '    if frame < ____:\n        print(f"frame {frame}: x = {x}, y = {y}")', '11',
          ('10', "That stops after frame 9, so only nine lines print."),
          ('FPS', "<code>FPS</code> is 60, so the probe would print 59 lines."),
          "<code>frame &lt; 11</code> is True for frames 1 to 10. After that the gate is False and the terminal stays quiet, however long the window is open."),
        Q(P11, "A grey square stays still, behind the ball. Which line draws it?",
          '    pygame.draw.rect(screen, BOX, (270, 190, 100, 100))',
          '    pygame.draw.____(screen, BOX, (270, 190, 100, 100))', 'rect',
          ('circle', "A circle needs a centre and a radius, not four numbers."),
          ('fill', "<code>fill</code> colours the whole screen. It is not in <code>pygame.draw</code>."),
          "The four numbers are x, y, width, and height. The numbers never change, so the square stays still.",
          note="Under <code>screen.fill(BG)</code>. It goes above the ball's line, so it is drawn first and the ball is drawn on top of it."),
        Q(P11, "Which line draws the ball?",
          '    pygame.draw.circle(screen, BALL, (x, y), R)',
          '    pygame.draw.circle(screen, BALL, (____, ____), R)', ('x', 'y'),
          (('vx', 'vy'), "Those are the speeds. The ball would be drawn near the top left corner and would never move."),
          (('320', '240'), "Then the ball would be drawn in the middle on every frame, whatever <code>x</code> and <code>y</code> are."),
          "The circle is drawn at the ball's centre, which changes on every frame. It is the last thing drawn, so it is on top."),
    ],
    "The ball starts at x = 320, y = 240 and moves 12 across and 7 down on each frame. What does the probe print on frame 10?",
    "x = 440, y = 310. Ten steps of 12 is 120, and ten steps of 7 is 70. The probe then stops, because <code>frame &lt; 11</code> is False from frame 11 on.",
    start=START11, run="headless", frames=60)

T14 = tool(
    "The three-bumper table, one line at a time",
    "The starting file is behind the button below: the main variables, <code>distance</code> from chunk 2, and a ball that bounces off the four walls. Run it first. Then add the bumpers.",
    P14,
    [
        Q(P14, "<code>hits</code> returns True when the ball touches a bumper. The bumpers are not all the same size, so the bumper's radius is a parameter. When do two circles touch?",
          'def hits(bx, by, px, py, radius):\n    return distance(bx, by, px, py) < BALL_R + radius',
          'def hits(bx, by, px, py, radius):\n    return distance(bx, by, px, py) < BALL_R ____ radius', '+',
          ('-', "That is True only when the ball's centre is deep inside the bumper."),
          ('*', "20 times 30 is 600, which is nearly the width of the window, so the ball would always be touching."),
          "Two circles touch when the distance between their centres is less than their two radiuses added together. The comparison gives True or False, and the function returns it.",
          note="Under <code>distance</code>, at the left edge, with an empty line above."),
        Q(P14, "The table needs a score, and a name that remembers whether the ball was touching a bumper on the frame before. What do they start as?",
          'score = 0\nwas_touching = 0',
          'score = ____\nwas_touching = ____', ('0', '0'),
          (('0', '1'), "That says the ball starts out touching a bumper, so the first real hit would not score."),
          (('100', '0'), "No bumper has been hit yet."),
          "No points yet, and the ball does not start on a bumper. 0 stands for not touching and 1 for touching.",
          note="Under <code>vy = 5</code>."),
        Q(P14, "On every frame, before the bumpers are checked, two names are set back. What to?",
          '    touching = 0\n    points = 0',
          '    touching = ____\n    points = ____', ('0', '0'),
          (('1', '0'), "That says the ball touches a bumper on every frame."),
          (('0', '100'), "The points are set by the bumper that is hit. Before the checks there are none."),
          "Each frame starts by saying the ball is touching nothing. The three gates below change that if it is.",
          note="After the four wall gates, one indentation level in, with an empty line above."),
        Q(P14, "The first bumper is at (160, 300). Which gate checks it, and what does it set?",
          '    if hits(x, y, 160, 300, BUMPER_R):\n        touching = 1\n        points = 100',
          '    if ____(x, y, 160, 300, BUMPER_R):\n        touching = ____\n        points = 100', ('hits', '1'),
          (('distance', '1'), "<code>distance</code> takes four numbers and returns a distance. The gate needs True or False."),
          (('hits', '0'), "0 means not touching, so a hit would never be noticed."),
          "<code>hits</code> gets the ball's centre, the bumper's centre, and the bumper's radius. When it returns True, the ball is touching, and this bumper is worth 100 points."),
        Q(P14, "The second bumper is at (480, 150) and is the same size. The third is at (320, 240), is bigger, and is worth less. What goes in the two blanks?",
          '    if hits(x, y, 480, 150, BUMPER_R):\n        touching = 1\n        points = 100\n    if hits(x, y, 320, 240, BIG_R):\n        touching = 1\n        points = 50',
          '    if hits(x, y, 480, 150, BUMPER_R):\n        touching = 1\n        points = 100\n    if hits(x, y, 320, 240, ____):\n        touching = 1\n        points = ____', ('BIG_R', '50'),
          (('BUMPER_R', '50'), "Then the ball would have to sink into the big bumper before it counted as a hit."),
          (('BIG_R', '100'), "The big bumper is easier to hit, so it is worth fewer points."),
          "Each bumper has its own gate with its own centre, radius, and points. <code>BIG_R</code> is 50, so the big bumper is touched from further away."),
        Q(P14, "A hit should score once, not once on every frame the ball stays on the bumper. Which test is True only on the first frame of a touch?",
          '    if touching == 1 and was_touching == 0:',
          '    if touching == 1 and was_touching == ____:', '0',
          ('1', "That is True from the second frame of a touch on, but not on the first frame."),
          ('2', "<code>was_touching</code> is only ever 0 or 1, so the test would never be True."),
          "The ball is touching now, and it was not touching on the frame before. That is only true on the frame the touch begins."),
        Q(P14, "A new touch. What four things happen?",
          '        vx = -vx\n        vy = -vy\n        score = score + points\n        print(f"hit worth {points}, score {score}")',
          '        vx = -vx\n        vy = ____\n        score = score + ____\n        print(f"hit worth {points}, score {score}")', ('-vy', 'points'),
          (('-vy', '100'), "Then the big bumper would score 100 too."),
          (('-vx', 'points'), "That stores the speed across in the speed down."),
          "Both speeds change sign, so the ball goes back the way it came. The score goes up by the points of the bumper that was hit, and the terminal prints it."),
        Q(P14, "The frame is nearly over. What has to be remembered for the next frame?",
          '    was_touching = touching',
          '    was_touching = ____', 'touching',
          ('0', "Then every frame of a touch would look like the first one, and one hit would score many times."),
          ('1', "Then the program would think the ball is always on a bumper, and nothing would ever score."),
          "On the next frame, <code>was_touching</code> says whether the ball was on a bumper on this one. The line is lined up with the <code>if</code>, so it runs on every frame, hit or not."),
        Q(P14, "The three bumpers have to be drawn. Which circle is the big one?",
          '    pygame.draw.circle(screen, (220, 38, 38), (160, 300), BUMPER_R)\n    pygame.draw.circle(screen, (220, 38, 38), (480, 150), BUMPER_R)\n    pygame.draw.circle(screen, (37, 99, 235), (320, 240), BIG_R)',
          '    pygame.draw.circle(screen, (220, 38, 38), (160, 300), BUMPER_R)\n    pygame.draw.circle(screen, (220, 38, 38), (480, 150), BUMPER_R)\n    pygame.draw.circle(screen, (37, 99, 235), (____, ____), BIG_R)', ('320', '240'),
          (('160', '300'), "That is the centre of the first bumper. The big one would be drawn on top of it."),
          (('50', '50'), "That is near the top left corner. The big bumper's gate checks the point (320, 240)."),
          "Each circle is drawn at the same centre and with the same radius that its gate checks, so what the player sees is what the program tests.",
          note="Under <code>screen.fill</code>, above the ball's line, so the ball is drawn on top."),
        Q(P14, "When the window closes, the terminal prints the final score. Which line?",
          'print(f"final score {score}")',
          'print(f"final score {____}")', 'score',
          ('points', "<code>points</code> holds the points of the last bumper checked, not the total."),
          ('touching', "That prints 0 or 1."),
          "The line is after the loop, at the left edge, above <code>pygame.quit()</code>, so it prints once."),
    ],
    "The ball hits the first bumper, then the big one, then the first again, and so on, five hits in all. What is the final score?",
    "400: three hits worth 100 and two worth 50. The second bumper is never touched on this run. A hit changes the sign of both speeds, so the ball goes back the way it came and keeps travelling between the same two bumpers. A real bounce, in the stretch exit, would send it somewhere new.",
    start=START14, run="headless", frames=400)

T15 = tool(
    "The cipher wheel, one line at a time",
    "Start with an empty file. The first line is the rack of 26 letters from chunk 3.",
    P15,
    [
        Q(P15, "The rack holds the alphabet in order, so each letter has a slot number. What kind of value is it?",
          'rack = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"',
          'rack = ____ABCDEFGHIJKLMNOPQRSTUVWXYZ____', ('"', '"'),
          (('[', ']'), "Square brackets make a list. Without quote marks inside them, Python looks for a variable with that long name, and there is none."),
          (('(', ')'), "Parentheses do not make text. Python looks for a variable with that long name, and there is none."),
          "The rack is one string of 26 characters. A is in slot 0 and Z is in slot 25."),
        Q(P15, "<code>shift</code> takes some text and a key and builds the secret one character at a time. What does the secret start as?",
          'def shift(text, key):\n    out = ""',
          'def shift(text, key):\n    out = ____', '""',
          ('rack', "Then the secret would start with the whole alphabet."),
          ('0', "<code>0</code> is a number. Adding a character to it gives an error."),
          "<code>out</code> is built by adding one character at a time, so it starts as empty text."),
        Q(P15, "For each character, the function finds its slot in the rack. Which lines?",
          '    for ch in text:\n        slot = rack.find(ch)',
          '    for ch in text:\n        slot = rack.____(ch)', 'find',
          ('upper', "<code>upper</code> changes letters to capitals. It does not say where a character is."),
          ('replace', "<code>replace</code> swaps one piece of text for another. It does not say where a character is."),
          "<code>find</code> returns the slot number of the character in the rack. For a character that is not in the rack, such as a space, it returns -1."),
        Q(P15, "A space is not in the rack. Which gate catches that, and what is added to <code>out</code>?",
          '        if slot < 0:\n            out = out + ch',
          '        if slot ____ 0:\n            out = out + ____', ('<', 'ch'),
          (('==', 'ch'), "Slot 0 is the letter A, so every A would be left as it is."),
          (('<', 'slot'), "<code>slot</code> is a number. Text plus a number gives an error."),
          "<code>find</code> returns -1 for a character that is not in the rack, and -1 is less than 0. That character is added as it is, so spaces come through unchanged."),
        Q(P15, "A letter is in the rack. Which slot does its secret letter come from?",
          '        else:\n            out = out + rack[(slot + key) % 26]',
          '        else:\n            out = out + rack[(slot + key) ____ 26]', '%',
          ('+', "That asks for a slot past the end of the rack, and Python gives an error."),
          ('-', "That gives a slot far to the left of where it should be."),
          "The letter moves <code>key</code> slots along the rack. The remainder after dividing by 26 wraps the slot round, so a slot past 25 starts again from 0. Z with a key of 3 comes out as C."),
        Q(P15, "The loop is done. How does the caller get the secret?",
          '    return out',
          '    return ____', 'out',
          ('text', "That returns the message as it came in, with nothing changed."),
          ('ch', "<code>ch</code> holds only the last character."),
          "<code>return</code> gives the finished string to the caller. The function returns the secret and does not print it, so the caller can store it or shift it again."),
        Q(P15, "The program asks for a message and a key. The message is changed to capitals, because the rack holds capitals. The key is used in arithmetic. Which line gets the key ready?",
          'message = input("Message: ")\nmessage = message.upper()\nkey = input("Key: ")\nkey = int(key)',
          'message = input("Message: ")\nmessage = message.upper()\nkey = input("Key: ")\nkey = ____(key)', 'int',
          ('input', "<code>input</code> would ask a second question."),
          ('shift', "<code>shift</code> needs some text and a key. It does not change text to a number."),
          "<code>input</code> gives text. <code>int</code> changes the type to a whole number, so the key can be added to a slot.",
          note="At the left edge, under the function, with an empty line above."),
        Q(P15, "Which line makes the secret?",
          'secret = shift(message, key)',
          'secret = shift(____, key)', 'message',
          ('rack', "That would encode the alphabet, not the message."),
          ('secret', "<code>secret</code> does not exist yet. This is the line that makes it."),
          "The call gives the message and the key to <code>shift</code> and is replaced by the string it returns."),
        Q(P15, "Decoding moves every letter back by the same number of slots. What key does that?",
          'print(f"Secret:  {secret}")\nprint(f"Decoded: {shift(secret, -key)}")',
          'print(f"Secret:  {secret}")\nprint(f"Decoded: {shift(secret, ____)}")', '-key',
          ('key', "That moves every letter forward again, further from the message."),
          ('0', "A key of 0 moves nothing, so the secret would be printed again."),
          "A key of 3 moves each letter 3 slots forward, and a key of -3 moves it 3 slots back. The remainder wraps a negative slot round to the end of the rack."),
        Q(P15, "A secret arrives and nobody knows the key. There are only 25 keys to try. Which loop tries them all?",
          'for k in range(1, 26):\n    print(k, shift("AOL JVPUZ HYL BUKLY AOL ZAHPYZ", -k))',
          'for k in range(1, ____):\n    print(k, shift("AOL JVPUZ HYL BUKLY AOL ZAHPYZ", -k))', '26',
          ('25', "<code>range</code> stops before its second number, so that tries keys 1 to 24 and misses one."),
          ('27', "A key of 26 moves every letter all the way round the rack, back to where it started."),
          "<code>range(1, 26)</code> gives 1 to 25. Each pass shifts the secret back by one more slot and prints the key next to the result. One of the 25 lines is readable."),
    ],
    "The player types meet at noon and a key of 3. Then 25 decodings of the other secret are printed. Which line can be read, and what was its key?",
    "Line 7: THE COINS ARE UNDER THE STAIRS. Every other line is a jumble. Nobody told the program the key was 7. A cipher with only 25 keys can be broken by trying them all.",
    run="py", stdin="meet at noon\n3\n")

BUILD_TOOLS = {1: [T1], 2: [T2], 3: [T3], 4: [T4], 6: [T6], 7: [T7], 9: [T9],
               10: [T10A, T10B], 11: [T11], 15: [T14], 16: [T15]}
del RUNS
