# Session 12: coin grab. Added November 2026 between the pygame window session and the
# room of tiles, which became session 13. A click picks up a stick figure and it follows the
# mouse until the next click puts it down; a coin jumps to a random spot when the figure
# touches it, and the terminal keeps the score.
#
# Chunks 1 to 3 are short terminal programs about pygame.Rect: its edges, the overlap
# test written by hand, and colliderect as the reveal after it. Chunk 4 is the first
# window file, chunk 5 draws a stick figure inside the player's Rect, and chunk 6 makes
# one click pick the figure up and the next click put it down. The build is one program in three tools, each a whole program that
# grows out of the one before:
#   tool 1  the coin jumps when the player touches it     (the floor exit)
#   tool 2  a score, and a win at ten coins               (the middle exit)
#   tool 3  three coins in a list, and a time limit       (the stretch exit)
# Every new line is a What goes next? question with a blank and three choices, kept
# here beside its step. Every program is run when the site is built. The window
# programs run without a screen: the mouse positions are fed in by render.py's
# harness, and the random numbers are seeded so the page is the same on every build.

import random

from builds import Q, swap

WIDTH = 600
HEIGHT = 400
PLAYER_SIZE = 50
COIN_SIZE = 30

# ------------------------------------------------------------------ the programs

RECT = '''import pygame

coin = pygame.Rect(300, 200, 30, 30)
print(coin.left, coin.right)
print(coin.top, coin.bottom)
print(coin.center)'''

BY_HAND = '''import pygame

player = pygame.Rect(280, 190, 50, 50)
coin = pygame.Rect(300, 280, 30, 30)

across = player.left < coin.right and coin.left < player.right
down = player.top < coin.bottom and coin.top < player.bottom
print(f"across {across}, down {down}, touching {across and down}")

coin.y = 200
down = player.top < coin.bottom and coin.top < player.bottom
print(f"across {across}, down {down}, touching {across and down}")'''

COLLIDE = '''import pygame

player = pygame.Rect(280, 190, 50, 50)
coin = pygame.Rect(300, 200, 30, 30)
print(player.colliderect(coin))

coin.x = 330
print(player.colliderect(coin))

coin.x = 329
print(player.colliderect(coin))'''

# chunk 4: the first window file
MOUSE = '''import pygame

# ---- main variables: every number the game depends on ----
WIDTH = 600
HEIGHT = 400
PLAYER_SIZE = 50
BG = (27, 41, 81)
PLAYER = (248, 250, 252)
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)

running = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0

    player.center = pygame.mouse.get_pos()

    screen.fill(BG)
    pygame.draw.rect(screen, PLAYER, player)
    pygame.display.flip()
    clock.tick(FPS)

print(f"centre {player.center}, left {player.left}, top {player.top}")
pygame.quit()'''

# chunk 5, and the file tool 1 starts from: the player is drawn as a stick figure
# that fits inside its Rect, 50 across and 50 down
STICK = MOUSE
STICK = swap(STICK, 'FPS = 60\n', '''FPS = 60

def draw_player(x, y):
    pygame.draw.circle(screen, PLAYER, (x, y + 10), 10, 3)
    pygame.draw.line(screen, PLAYER, (x, y + 20), (x, y + 35), 3)
    pygame.draw.rect(screen, PLAYER, (x - 20, y + 25, 40, 3))
    pygame.draw.line(screen, PLAYER, (x, y + 35), (x - 15, y + 50), 3)
    pygame.draw.line(screen, PLAYER, (x, y + 35), (x + 15, y + 50), 3)
''')
STICK = swap(STICK, '    pygame.draw.rect(screen, PLAYER, player)\n',
             '    draw_player(player.centerx, player.top)\n')

# chunk 6, and the file tool 1 starts from: one click picks the figure up, and the
# next click puts it down, so a click is free for something else while it is down
CLICK = STICK
CLICK = swap(CLICK, 'player = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)\n',
             'player = pygame.Rect(75, 175, PLAYER_SIZE, PLAYER_SIZE)\nholding = 0\n')
CLICK = swap(CLICK, '''while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0

    player.center = pygame.mouse.get_pos()
''', '''while running:
    click = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = 1

    mouse = pygame.mouse.get_pos()
    if click == 1 and holding == 1:
        holding = 0
        print("put down")
    elif click == 1 and player.collidepoint(mouse):
        holding = 1
        print("picked up")
    if holding == 1:
        player.center = mouse
''')
CLICK = swap(CLICK, 'print(f"centre {player.center}, left {player.left}, top {player.top}")\n',
             'print(f"centre {player.center}, holding {holding}")\n')

TOOL1 = CLICK
TOOL1 = swap(TOOL1, 'import pygame\n\n# ----', 'import random\nimport pygame\n\n# ----')
TOOL1 = swap(TOOL1, 'PLAYER_SIZE = 50\n', 'PLAYER_SIZE = 50\nCOIN_SIZE = 30\n')
TOOL1 = swap(TOOL1, 'PLAYER = (248, 250, 252)\n', 'PLAYER = (248, 250, 252)\nCOIN = (252, 211, 77)\n')
TOOL1 = swap(TOOL1, 'PLAYER_SIZE)\nholding = 0\n',
             'PLAYER_SIZE)\nholding = 0\n'
             'coin = pygame.Rect(300, 200, COIN_SIZE, COIN_SIZE)\n')
TOOL1 = swap(TOOL1, '        player.center = mouse\n', '''        player.center = mouse
    if player.colliderect(coin):
        coin.x = random.randint(0, WIDTH - COIN_SIZE)
        coin.y = random.randint(0, HEIGHT - COIN_SIZE)
        print(f"grabbed, the coin is now at {coin.x}, {coin.y}")
''')
TOOL1 = swap(TOOL1, '    screen.fill(BG)\n', '    screen.fill(BG)\n    pygame.draw.rect(screen, COIN, coin)\n')

TOOL2 = TOOL1
TOOL2 = swap(TOOL2, 'COIN_SIZE = 30\n', 'COIN_SIZE = 30\nGOAL = 10\n')
TOOL2 = swap(TOOL2, 'COIN = (252, 211, 77)\n', 'COIN = (252, 211, 77)\nWIN = (29, 91, 57)\n')
TOOL2 = swap(TOOL2, 'coin = pygame.Rect(300, 200, COIN_SIZE, COIN_SIZE)\n',
             'coin = pygame.Rect(300, 200, COIN_SIZE, COIN_SIZE)\n\n'
             'score = 0\nplaying = 1\nbackground = BG\n')
TOOL2 = swap(TOOL2, '    if player.colliderect(coin):\n', '    if playing == 1 and player.colliderect(coin):\n')
TOOL2 = swap(TOOL2, '        print(f"grabbed, the coin is now at {coin.x}, {coin.y}")\n',
             '''        score = score + 1
        print(f"score {score}")
    if playing == 1 and score >= GOAL:
        playing = 0
        background = WIN
        print(f"You win with {score} coins.")
''')
TOOL2 = swap(TOOL2, '    screen.fill(BG)\n', '    screen.fill(background)\n')
TOOL2 = swap(TOOL2, 'print(f"centre {player.center}, holding {holding}")\n',
             'print(f"final score {score}")\n')

TOOL3 = TOOL2
TOOL3 = swap(TOOL3, 'GOAL = 10\n', 'GOAL = 10\nSECONDS = 30\n')
TOOL3 = swap(TOOL3, 'WIN = (29, 91, 57)\n', 'WIN = (29, 91, 57)\nLOSE = (156, 43, 34)\n')
TOOL3 = swap(TOOL3, 'coin = pygame.Rect(300, 200, COIN_SIZE, COIN_SIZE)\n', '''coins = [
    pygame.Rect(100, 100, COIN_SIZE, COIN_SIZE),
    pygame.Rect(300, 200, COIN_SIZE, COIN_SIZE),
    pygame.Rect(500, 300, COIN_SIZE, COIN_SIZE),
]
''')
TOOL3 = swap(TOOL3, 'background = BG\n', 'background = BG\nframe = 0\n')
TOOL3 = swap(TOOL3, '''        player.center = mouse
    if playing == 1 and player.colliderect(coin):
        coin.x = random.randint(0, WIDTH - COIN_SIZE)
        coin.y = random.randint(0, HEIGHT - COIN_SIZE)
        score = score + 1
        print(f"score {score}")
''', '''        player.center = mouse
    frame = frame + 1
    for coin in coins:
        if playing == 1 and player.colliderect(coin):
            coin.x = random.randint(0, WIDTH - COIN_SIZE)
            coin.y = random.randint(0, HEIGHT - COIN_SIZE)
            score = score + 1
            print(f"score {score}")
''')
TOOL3 = swap(TOOL3, '''        print(f"You win with {score} coins.")
''', '''        print(f"You win with {score} coins.")
    if playing == 1 and frame == SECONDS * FPS:
        playing = 0
        background = LOSE
        print(f"Time is up. You got {score} coins.")
''')
TOOL3 = swap(TOOL3, '    pygame.draw.rect(screen, COIN, coin)\n',
             '    for coin in coins:\n        pygame.draw.rect(screen, COIN, coin)\n')

# the extension: the two randint lines get a name
MOVE_COIN = '''import random
import pygame

WIDTH = 600
HEIGHT = 400
COIN_SIZE = 30

def move_coin(coin):
    coin.x = random.randint(0, WIDTH - COIN_SIZE)
    coin.y = random.randint(0, HEIGHT - COIN_SIZE)

coin = pygame.Rect(300, 200, COIN_SIZE, COIN_SIZE)
print(coin.x, coin.y)

move_coin(coin)
print(coin.x, coin.y)

print(move_coin(coin))'''

HINGE = '''score = 0
touching = True
for frame in range(60):
    if touching:
        score = score + 1
print(score)'''

for _name, _prog in (("MOUSE", MOUSE), ("STICK", STICK), ("CLICK", CLICK), ("TOOL1", TOOL1), ("TOOL2", TOOL2), ("TOOL3", TOOL3)):
    for _ln in _prog.split("\n"):
        assert len(_ln) <= 72, _name + ": a line is wider than the code box: " + _ln


# ------------------------------------------------------------------ the mouse, for the build runs

def chase(seed, starts, visits, goal=None, first=3, gap=3):
    """Mouse positions that put the player on a coin `visits` times, for a headless run.

    The window programs pick each new coin spot at random, so where the mouse has to go
    next depends on the random numbers. This plays the game's own rule with the same
    seed and the same two randint calls in the same order, and writes down where the
    mouse went. Visit k happens on frame first + k * gap: the mouse goes to the middle
    of a coin and stays there until the next visit. It returns the harness's inject
    list and the number of frames played, or None if a coin ever landed under a player
    that was standing still, because the page says how many times the mouse went to a
    coin and each visit has to be exactly one grab.
    """
    rng = random.Random(seed)
    coins = [[x, y] for x, y in starts]
    # frame 1: a click on the figure where it starts, centre (100, 200), picks it up
    inject = [[1, "CLICK", 100, 200]]
    mouse = (100, 200)
    grabs = 0
    total = first + visits * gap
    for frame in range(1, total + 1):
        k = (frame - first) // gap
        if frame >= first and (frame - first) % gap == 0 and k < visits:
            target = coins[k % len(coins)]
            mouse = (target[0] + COIN_SIZE // 2, target[1] + COIN_SIZE // 2)
            inject.append([frame, "MOUSE", mouse[0], mouse[1]])
        left = mouse[0] - PLAYER_SIZE // 2
        top = mouse[1] - PLAYER_SIZE // 2
        for c in coins:
            across = left < c[0] + COIN_SIZE and c[0] < left + PLAYER_SIZE
            down = top < c[1] + COIN_SIZE and c[1] < top + PLAYER_SIZE
            if across and down and (goal is None or grabs < goal):
                c[0] = rng.randint(0, WIDTH - COIN_SIZE)
                c[1] = rng.randint(0, HEIGHT - COIN_SIZE)
                grabs = grabs + 1
    wanted = visits if goal is None else min(visits, goal)
    if grabs != wanted:
        return None
    return inject, total


def chase_or_stop(seed, *args, **kwargs):
    got = chase(seed, *args, **kwargs)
    assert got, "seed %d gives an extra grab in this run; pick another seed" % seed
    return got


SEED1, SEED2, SEED3 = 2, 2, 2
# tool 1: the mouse goes to the coin once and stays there for half a second
INJECT1, TOTAL1 = chase_or_stop(SEED1, [(300, 200)], 1, gap=30)
# tool 2: the mouse goes to the coin eleven times; the game is won at ten
INJECT2, TOTAL2 = chase_or_stop(SEED2, [(300, 200)], 11, goal=10)
# tool 3: the mouse goes to a coin four times, then stays where it is until time is up
INJECT3, TOTAL3 = chase_or_stop(SEED3, [(100, 100), (300, 200), (500, 300)], 4)
# the harness plays one more frame than it is asked for: the frame that carries the QUIT
FRAMES1 = TOTAL1 - 1
FRAMES2 = TOTAL2 - 1
FRAMES3 = 30 * 60 + 10


# ------------------------------------------------------------------ the figures

def rect_figure():
    """The coin Rect(300, 200, 30, 30) drawn six times its size, with every edge named."""
    return ('<svg viewBox="0 0 660 300" width="100%" role="img" aria-label="A square coin '
            'that starts at x = 300, y = 200 and is 30 wide and 30 tall. Its left edge is at '
            '300, its right edge at 330, its top edge at 200, its bottom edge at 230, and its '
            'centre at 315, 215" '
            'style="max-width:660px;display:block;margin:0 0 16px;font-family:JetBrains Mono,'
            'monospace;font-size:13px">'
            '<rect x="150" y="70" width="180" height="180" fill="#FCD34D" stroke="#17181B" stroke-width="5"/>'
            '<circle cx="150" cy="70" r="5" fill="#17181B"/>'
            '<text x="20" y="34" fill="#17181B" font-weight="700">starts at x = 300, y = 200</text>'
            '<circle cx="240" cy="160" r="5" fill="#17181B"/>'
            '<text x="170" y="184" fill="#17181B" font-weight="700">center (315, 215)</text>'
            '<text x="196" y="56" fill="#9C2B22" font-weight="700">top 200</text>'
            '<text x="182" y="272" fill="#9C2B22" font-weight="700">bottom 230</text>'
            '<text x="64" y="164" fill="#1D5B39" font-weight="700">left 300</text>'
            '<text x="342" y="164" fill="#1D5B39" font-weight="700">right 330</text>'
            '<text x="450" y="80" fill="#17181B" font-weight="700">Rect(x, y, w, h)</text>'
            '<text x="450" y="110" fill="#4A4D53">left = x</text>'
            '<text x="450" y="132" fill="#4A4D53">right = x + w</text>'
            '<text x="450" y="154" fill="#4A4D53">top = y</text>'
            '<text x="450" y="176" fill="#4A4D53">bottom = y + h</text>'
            '<text x="450" y="216" fill="#4A4D53">the picture is six</text>'
            '<text x="450" y="238" fill="#4A4D53">times the real size</text>'
            '</svg>')


def overlap_figure():
    """Chunk 2's player and its coin in both places, at twice their size."""
    k = 2

    def sx(x):
        return 40 + (x - 260) * k

    def sy(y):
        return 30 + (y - 180) * k

    out = ['<svg viewBox="0 0 660 330" width="100%" role="img" aria-label="The player is a '
           'square from 280 to 330 across and from 190 to 240 down. A coin from 300 to 330 '
           'across is drawn twice: at y = 280, below the player, where the two do not '
           'touch, and at y = 200, inside the player, where they overlap" '
           'style="max-width:660px;display:block;margin:0 0 16px;font-family:JetBrains Mono,'
           'monospace;font-size:13px">']
    # the player
    out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#F8FAFC" stroke="#17181B" stroke-width="5"/>'
               % (sx(280), sy(190), 50 * k, 50 * k))
    out.append('<text x="%d" y="%d" fill="#17181B" font-weight="700">player</text>' % (sx(280), sy(190) - 10))
    # the coin at y = 200, overlapping
    out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#FCD34D" stroke="#17181B" stroke-width="3"/>'
               % (sx(300), sy(200), 30 * k, 30 * k))
    # the coin at y = 280, apart
    out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#FCD34D" stroke="#17181B" stroke-width="3"/>'
               % (sx(300), sy(280), 30 * k, 30 * k))
    # labels to the right of each thing
    tx = sx(330) + 24
    out.append('<text x="%d" y="%d" fill="#17181B" font-weight="700">player: 280 to 330 across, 190 to 240 down</text>' % (tx, sy(190) + 14))
    out.append('<text x="%d" y="%d" fill="#1D5B39" font-weight="700">coin at y = 200: 200 to 230 down</text>' % (tx, sy(190) + 50))
    out.append('<text x="%d" y="%d" fill="#1D5B39">inside 190 to 240, so they overlap</text>' % (tx, sy(190) + 70))
    out.append('<text x="%d" y="%d" fill="#9C2B22" font-weight="700">coin at y = 280: 280 to 310 down</text>' % (tx, sy(280) + 24))
    out.append('<text x="%d" y="%d" fill="#9C2B22">it starts after 240, so they do not touch</text>' % (tx, sy(280) + 44))
    out.append('<text x="40" y="316" fill="#4A4D53">both coins: 300 to 330 across. The picture is twice the real size.</text>')
    out.append('</svg>')
    return "".join(out)



# ------------------------------------------------------------------ the opener's pictures
# The opener reviews where things are in a pygame window. Every picture is the game's
# window, 600 wide and 400 tall, drawn at three quarters of its size with a grid line
# every 100 pixels, so a spot can be read off the picture.

INK, SOFT, GRID, GREEN, CLAY, GOLD = "#17181B", "#4A4D53", "#D3CBB8", "#1D5B39", "#9C2B22", "#FCD34D"
K = 0.75
OX, OY = 80, 60


def _px(x):
    return OX + x * K


def _py(y):
    return OY + y * K


def _arrow(x1, y1, x2, y2, color, dashed=False, width=3):
    """A line with a head at its end, in picture coordinates."""
    dx, dy = x2 - x1, y2 - y1
    n = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / n, dy / n
    bx, by = x2 - ux * 12, y2 - uy * 12
    dash = ' stroke-dasharray="8 6"' if dashed else ''
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%d"%s/>'
            '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
            % (x1, y1, bx, by, color, width, dash, x2, y2, bx - uy * 7, by + ux * 7,
               bx + uy * 7, by - ux * 7, color))


def _text(x, y, words, color=INK, anchor="start", bold=True):
    return ('<text x="%.1f" y="%.1f" fill="%s" text-anchor="%s"%s>%s</text>'
            % (x, y, color, anchor, ' font-weight="700"' if bold else '', words))


def window_figure(aria, marks, axes=False):
    """The 600 by 400 window with its grid and numbers, and marks drawn on it.

    marks are pieces of SVG already placed with _px and _py.
    """
    out = ['<svg viewBox="0 0 680 400" width="100%" role="img" aria-label="' + aria + '" '
           'style="max-width:680px;display:block;margin:0 0 16px;font-family:JetBrains Mono,'
           'monospace;font-size:14px">']
    out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#FFFDF7"/>'
               % (_px(0), _py(0), 600 * K, 400 * K))
    for x in range(100, 600, 100):
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.5"/>'
                   % (_px(x), _py(0), _px(x), _py(400), GRID))
    for y in range(100, 400, 100):
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.5"/>'
                   % (_px(0), _py(y), _px(600), _py(y), GRID))
    out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="%s" stroke-width="4"/>'
               % (_px(0), _py(0), 600 * K, 400 * K, INK))
    for x in range(0, 601, 100):
        out.append(_text(_px(x), _py(0) - 10, str(x), SOFT, "middle", False))
    for y in range(0, 401, 100):
        out.append(_text(_px(0) - 10, _py(y) + 5, str(y), SOFT, "end", False))
    if axes:
        out.append(_arrow(_px(0), 18, _px(600) + 40, 18, GREEN))
        out.append(_text(_px(600) + 50, 23, "x", GREEN))
        out.append(_text(_px(300), 13, "x gets bigger going right", GREEN, "middle"))
        out.append(_arrow(24, _py(0), 24, _py(400) + 30, CLAY))
        out.append(_text(24, _py(400) + 48, "y", CLAY, "middle"))
        out.append('<text x="14" y="%.1f" fill="%s" font-weight="700" text-anchor="middle" '
                   'transform="rotate(90 14 %.1f)">y gets bigger going down</text>'
                   % (_py(200), CLAY, _py(200)))
    out.extend(marks)
    out.append('</svg>')
    return "".join(out)


def _dot(x, y, color=INK):
    return '<circle cx="%.1f" cy="%.1f" r="7" fill="%s"/>' % (_px(x), _py(y), color)


def map_figure():
    """The window, its two arrows, its four corners, and its middle."""
    marks = [_dot(0, 0), _text(_px(0) + 12, _py(0) + 24, "(0, 0)"),
             _dot(600, 0), _text(_px(600) - 12, _py(0) + 24, "(600, 0)", anchor="end"),
             _dot(0, 400), _text(_px(0) + 12, _py(400) - 12, "(0, 400)"),
             _dot(600, 400), _text(_px(600) - 12, _py(400) - 12, "(600, 400)", anchor="end"),
             _dot(300, 200, GREEN), _text(_px(300) + 12, _py(200) - 10, "(300, 200), the middle", GREEN)]
    return window_figure("A pygame window 600 wide and 400 tall. The top left corner is (0, 0). "
                         "The top right corner is (600, 0), the bottom left corner is (0, 400), and "
                         "the bottom right corner is (600, 400). The middle is (300, 200). x gets "
                         "bigger going right, and y gets bigger going down", marks, axes=True)


def two_ways_figure():
    """Maths class and a pygame window side by side: y goes up in one and down in the other."""
    out = ['<svg viewBox="0 0 680 290" width="100%" role="img" aria-label="Two pictures side by '
           'side. In maths class, (0, 0) is the bottom left corner, x goes right and y goes up. In '
           'a pygame window, (0, 0) is the top left corner, x goes right and y goes down" '
           'style="max-width:680px;display:block;margin:0 0 16px;font-family:JetBrains Mono,'
           'monospace;font-size:14px">']
    # maths class
    out.append(_text(150, 24, "In maths class", INK, "middle"))
    out.append('<rect x="40" y="50" width="220" height="180" fill="#FFFDF7" stroke="%s" stroke-width="3"/>' % GRID)
    out.append(_arrow(40, 230, 250, 230, GREEN))
    out.append(_text(256, 250, "x", GREEN))
    out.append(_arrow(40, 230, 40, 58, CLAY))
    out.append(_text(32, 52, "y", CLAY, "end"))
    out.append('<circle cx="40" cy="230" r="7" fill="%s"/>' % INK)
    out.append(_text(40, 256, "(0, 0)", INK, "middle"))
    out.append(_text(150, 284, "y gets bigger going up", CLAY, "middle"))
    # pygame
    out.append(_text(510, 24, "In a pygame window", INK, "middle"))
    out.append('<rect x="400" y="50" width="220" height="180" fill="#FFFDF7" stroke="%s" stroke-width="4"/>' % INK)
    out.append(_arrow(400, 50, 610, 50, GREEN))
    out.append(_text(616, 46, "x", GREEN))
    out.append(_arrow(400, 50, 400, 222, CLAY))
    out.append(_text(392, 238, "y", CLAY, "end"))
    out.append('<circle cx="400" cy="50" r="7" fill="%s"/>' % INK)
    out.append(_text(408, 74, "(0, 0)"))
    out.append(_text(510, 284, "y gets bigger going down", CLAY, "middle"))
    out.append('</svg>')
    return "".join(out)


def find_figure():
    """How to find (450, 100): across from the corner, then down."""
    marks = [_arrow(_px(0), _py(0), _px(450), _py(0), GREEN, dashed=True, width=4),
             _text(_px(225), _py(0) + 24, "1. go 450 across", GREEN, "middle"),
             _arrow(_px(450), _py(0), _px(450), _py(100), CLAY, dashed=True, width=4),
             _text(_px(450) - 12, _py(50) + 5, "2. go 100 down", CLAY, "end"),
             _dot(0, 0), _dot(450, 100),
             _text(_px(450) + 12, _py(100) + 24, "(450, 100)")]
    return window_figure("To find (450, 100), start at the top left corner, go 450 across to the "
                         "right, then go 100 down. The spot is near the top right of the window",
                         marks)


def tile_figure():
    """Session 6's tile (40, 40, 200, 120): its corner, its size, and its edges."""
    x, y, w, h = 40, 40, 200, 120
    marks = ['<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#F2B8B5" stroke="%s" stroke-width="3"/>'
             % (_px(x), _py(y), w * K, h * K, INK),
             _dot(x, y),
             _text(_px(x) + 12, _py(y) + 24, "(40, 40)"),
             _text(_px(x + w / 2), _py(y + h / 2) + 12, "200 wide", INK, "middle", False),
             _text(_px(x + w / 2), _py(y + h / 2) + 32, "120 tall", INK, "middle", False),
             _arrow(_px(x + w) + 50, _py(y + h / 2), _px(x + w) + 6, _py(y + h / 2), GREEN),
             _text(_px(x + w) + 56, _py(y + h / 2) - 4, "right edge 240", GREEN),
             _text(_px(x + w) + 56, _py(y + h / 2) + 16, "(40 + 200)", GREEN, bold=False),
             _arrow(_px(x + w / 2), _py(y + h) + 44, _px(x + w / 2), _py(y + h) + 6, CLAY),
             _text(_px(x + w / 2), _py(y + h) + 62, "bottom edge 160", CLAY, "middle"),
             _text(_px(x + w / 2), _py(y + h) + 82, "(40 + 120)", CLAY, "middle", False)]
    return window_figure("The tile (40, 40, 200, 120). Its top left corner is at (40, 40). It is "
                         "200 wide and 120 tall. Its right edge is at 40 + 200, which is 240, and "
                         "its bottom edge is at 40 + 120, which is 160", marks)


def move_figure(before, after, words, aria):
    """A dot before and after it moves, with an arrow between them."""
    (x1, y1), (x2, y2) = before, after
    dx, dy = x2 - x1, y2 - y1
    n = (dx * dx + dy * dy) ** 0.5
    marks = [_dot(x1, y1, SOFT), _dot(x2, y2, GREEN),
             _arrow(_px(x1), _py(y1), _px(x2) - dx / n * 10, _py(y2) - dy / n * 10, GREEN),
             _text(_px(x1) + 14, _py(y1) + 5, "before (%d, %d)" % before, SOFT),
             _text(_px(x2) + 14, _py(y2) + 5, "after (%d, %d)" % after, GREEN),
             _text(_px(x1) - 14, _py((y1 + y2) / 2) + 5, words, GREEN, "end", False)]
    return window_figure(aria, marks)


def spots_figure(spots, aria):
    """Named dots on the window: (x, y, label, color)."""
    marks = []
    for x, y, words, color in spots:
        marks.append(_dot(x, y, color))
        if x > 400:
            marks.append(_text(_px(x) - 14, _py(y) + 5, words, color, "end"))
        else:
            marks.append(_text(_px(x) + 14, _py(y) + 5, words, color))
    return window_figure(aria, marks)


def strip_figure():
    """The rectangle (0, 300, 600, 100) along the bottom of the window."""
    marks = ['<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="3"/>'
             % (_px(0), _py(300), 600 * K, 100 * K, GOLD, INK),
             _dot(0, 300),
             _text(_px(0) + 12, _py(300) - 10, "(0, 300), its top left corner"),
             _text(_px(300), _py(350) + 5, "300 + 100 = 400, the bottom of the window", INK, "middle")]
    return window_figure("The rectangle (0, 300, 600, 100) is a strip along the bottom of the "
                         "window. It starts 300 down and is 100 tall, so its bottom edge is at "
                         "400, the bottom of the window", marks)

# ------------------------------------------------------------------ the build

HOW12 = ("Each new line is a question for the room before it goes on the screen. Each question "
         "shows the line with a blank and three choices. Ask the room to pick before you click. "
         "A wrong choice says why it does not fit, and the right choice shows the finished line "
         "and why it is right.")

TOOLS12 = [
    {"title": "Tool 1: the coin jumps when you touch it",
     "intro": "The starting file is chunk 6's program: the stick figure you pick up with one click and put down with the next. It is behind the button below. Now the window gets a coin: a gold square that stays still until the player touches it, then jumps to a spot picked at random. The terminal says where it went. " + HOW12,
     "start": CLICK,
     "places": [('Line 1', '<code>import random</code>'), ('Main variables', '<code>COIN_SIZE</code> and <code>COIN</code>'), ('Above the loop', "the coin's Rect"), ('Inside the loop, after the player moves', 'the gate that asks whether the player touches the coin, and its three lines'), ('Inside the loop, after <code>screen.fill</code>', 'the line that draws the coin')],
     "whole": "Show the whole program",
     "code": TOOL1,
     "run": "headless", "frames": FRAMES1, "seed": SEED1, "inject": INJECT1,
     "steps": [
         Q(TOOL1, "The coin will jump to a spot picked at random. Which line lets the program pick random numbers?",
           'import random',
           'import ____', 'random',
           ('randint', "Python has no library called <code>randint</code>. <code>randint</code> is a function inside the <code>random</code> library."),
           ('pygame', "<code>pygame</code> is already imported, on the next line. The random numbers come from a different library."),
           "<code>random</code> is the library from session 3. Importing it lets the program call <code>random.randint</code> further down.",
           note="This is the new first line of the file, above <code>import pygame</code>."),
         Q(TOOL1, "The coin is a square 30 across. Its size is added to the main variables. Which name holds it?",
           'COIN_SIZE = 30',
           '____ = 30', 'COIN_SIZE',
           ('COIN', "<code>COIN</code> is the name for the coin's colour, a few lines further down."),
           ('coin_size', "The main variables have names in capitals, so they stand out from the variables that change while the game runs."),
           "<code>COIN_SIZE</code> is how wide and how tall the coin is.",
           note="Under <code>PLAYER_SIZE</code>."),
         Q(TOOL1, "The coin is gold. Its colour is added to the main variables too. Which name holds it?",
           'COIN = (252, 211, 77)',
           '____ = (252, 211, 77)', 'COIN',
           ('COIN_SIZE', "<code>COIN_SIZE</code> already holds the coin's size, 30. One name holds one value."),
           ('coin', "The small name <code>coin</code> is for the coin's Rect, further down. The main variables have names in capitals."),
           "A lot of red, a lot of green, and a little blue make gold.",
           note="Under <code>PLAYER</code>."),
         Q(TOOL1, "The coin is a Rect, like the player. It starts at x = 300, y = 200. What are its width and its height?",
           'coin = pygame.Rect(300, 200, COIN_SIZE, COIN_SIZE)',
           'coin = pygame.Rect(300, 200, ____, ____)', ('COIN_SIZE', 'COIN_SIZE'),
           (('PLAYER_SIZE', 'PLAYER_SIZE'), "Then the coin would be 50 across, as big as the player."),
           (('330', '230'), "The last two numbers are the width and the height, not the right edge and the bottom edge. That coin would be 330 wide."),
           "The four numbers are x, y, width, and height. The coin is a square, so its width and its height are the same variable.",
           note="Under the <code>player</code> line, above the loop. Above the loop, it runs once. Inside the loop, the coin would be put back at 300, 200 on every frame."),
         Q(TOOL1, "On every frame, after the player has moved, the program asks one question: is the player touching the coin? Which gate asks it?",
           '    if player.colliderect(coin):',
           '    if ____.colliderect(____):', ('player', 'coin'),
           (('player', 'player'), "A rectangle overlaps itself, so this is True on every frame."),
           (('screen', 'coin'), "<code>screen</code> is the window, not a Rect. It has no <code>colliderect</code>, so Python gives an error."),
           "<code>colliderect</code> is the test from chunk 3. It gives True when the two rectangles overlap. The gate is inside the frame loop, so the question is asked 60 times a second.",
           note="Under the gate <code>if holding == 1:</code> and its line, lined up with its <code>if</code>."),
         Q(TOOL1, "The player is touching the coin. The coin jumps to a new spot. The window is 600 wide and 400 tall. Which variable limits x, and which limits y?",
           '        coin.x = random.randint(0, WIDTH - COIN_SIZE)\n        coin.y = random.randint(0, HEIGHT - COIN_SIZE)',
           '        coin.x = random.randint(0, ____ - COIN_SIZE)\n        coin.y = random.randint(0, ____ - COIN_SIZE)', ('WIDTH', 'HEIGHT'),
           (('HEIGHT', 'WIDTH'), "Those are swapped. x goes across, so the width limits it. With y as large as 570, the coin could land below the bottom of the window, which is at 400."),
           (('COIN_SIZE', 'COIN_SIZE'), "<code>COIN_SIZE - COIN_SIZE</code> is 0. <code>random.randint(0, 0)</code> gives 0 every time, so the coin would go to the top left corner and stay there."),
           "<code>WIDTH - COIN_SIZE</code> is 570. A coin whose left edge is at 570 has its right edge at 600, the right edge of the window. A larger x would put part of the coin outside. The same goes for y: <code>HEIGHT - COIN_SIZE</code> is 370."),
         Q(TOOL1, "Words go in the terminal. Which line says where the coin went?",
           '        print(f"grabbed, the coin is now at {coin.x}, {coin.y}")',
           '        print(f"grabbed, the coin is now at {____}, {____}")', ('coin.x', 'coin.y'),
           (('player.x', 'player.y'), "That prints where the player's top left corner is, not where the coin went."),
           (('x', 'y'), "This program has no variables called <code>x</code> and <code>y</code>. Python gives a NameError."),
           "The print is inside the gate, after the two lines that move the coin, so it prints the new spot, once for each grab."),
         Q(TOOL1, "The coin has to be drawn on every frame. Which line draws it?",
           '    pygame.draw.rect(screen, COIN, coin)',
           '    pygame.draw.rect(screen, ____, ____)', ('COIN', 'coin'),
           (('coin', 'COIN'), "Those are swapped. The colour goes second and the rectangle goes third. Swapped, Python gives an error."),
           (('COIN', 'player'), "That draws a gold square where the player is. The coin itself is never drawn."),
           "<code>COIN</code> in capitals is the colour, and <code>coin</code> in small letters is the Rect. Python treats them as two different names.",
           note="Under <code>screen.fill(BG)</code> and above the line <code>draw_player(player.centerx, player.top)</code>. The player is drawn after the coin, so the player is on top."),
     ],
     "predict": "The mouse sits on the coin for half a second. How many times does <code>grabbed</code> print?",
     "reveal": "On the frame the mouse arrives, the gate is True and the coin jumps to 57, 46. After that the coin is somewhere else, so the gate is False. The spot is picked at random, so your numbers will be different. If a new spot lands under the player, the coin jumps again on the next frame. This is the floor exit.",
     "pick": {"right": "Once", "wrong": [("About 30 times, once a frame", "The coin jumps away on the first frame, so on the next frame the player is not touching it and the gate is False."), ("Never", "The mouse is on the coin, so <code>colliderect</code> is True on that frame.")]},
     },
    {"title": "Tool 2: a score, and a win at ten coins",
     "intro": "The game needs a score and a way to end. Every grab adds 1 to the score, and the terminal prints it. At ten coins the game is won: the window turns green, and touching the coin does nothing any more.",
     "start": TOOL1,
     "places": [('Main variables', '<code>GOAL</code> and <code>WIN</code>'), ('Above the loop', '<code>score</code>, <code>playing</code>, and <code>background</code>'), ('Inside the loop', 'a second test in the coin gate, the score lines in place of the print, and the win gate'), ('Inside the loop, the drawing', '<code>screen.fill</code> uses <code>background</code>'), ('After the loop', 'the last print')],
     "whole": "Show the whole program",
     "code": TOOL2,
     "run": "headless", "frames": FRAMES2, "seed": SEED2, "inject": INJECT2,
     "steps": [
         Q(TOOL2, "Ten coins wins the game. That number is added to the main variables. What does <code>GOAL</code> hold?",
           'GOAL = 10',
           'GOAL = ____', '10',
           ('0', "The score starts at 0, so with a goal of 0 the game would be won on the first frame, before any coin is grabbed."),
           ('"10"', "With quote marks it is text. Comparing the score with text gives an error."),
           "The goal has a name, so it can be changed in one place.",
           note="Under <code>COIN_SIZE</code>."),
         Q(TOOL2, "When the game is won, the window turns dark green. Which name holds that colour?",
           'WIN = (29, 91, 57)',
           '____ = (29, 91, 57)', 'WIN',
           ('GOAL', "<code>GOAL</code> already holds the number of coins that wins, 10."),
           ('BG', "<code>BG</code> is the dark blue the window starts with. Changing it would make the window green from the first frame."),
           "<code>WIN</code> is a dark green. The win gate will fill the window with it.",
           note="Under <code>COIN</code>."),
         Q(TOOL2, "Three variables start the game. <code>score</code> counts coins. <code>playing</code> is 1 while the game is being played and 0 when it is over. <code>background</code> is the colour the window is filled with. What do the first two start as?",
           'score = 0\nplaying = 1\nbackground = BG',
           'score = ____\nplaying = ____\nbackground = BG', ('0', '1'),
           (('1', '1'), "No coin has been grabbed yet, so the score cannot start at 1."),
           (('0', '0'), "<code>playing = 0</code> means the game is over. No coin could be grabbed."),
           "The three lines are above the frame loop, so they run once. Inside the loop, the score would go back to 0 on every frame. <code>playing</code> works the way <code>running</code> does: 1 for yes, 0 for no.",
           note="Under the <code>coin</code> line, with an empty line above."),
         Q(TOOL2, "After a win, touching the coin must do nothing. So the gate needs two tests: the game is being played, and the player is touching the coin. Which word joins two tests on one line?",
           '    if playing == 1 and player.colliderect(coin):',
           '    if playing == 1 ____ player.colliderect(coin):', 'and',
           ('or', "With <code>or</code>, one True test is enough. The gate would be True on every frame of the game, touching or not, and the coin would jump 60 times a second."),
           ('if', "One gate has one <code>if</code>. Two tests on the same line are joined with <code>and</code>."),
           "Both tests have to be True. When <code>playing</code> is 0 the first test is False, so the coin stays where it is. This is one flat gate, not a gate inside a gate."),
         Q(TOOL2, "The print that said grabbed is replaced by two lines. What happens to the score, and what does the terminal print?",
           '        score = score + 1\n        print(f"score {score}")',
           '        score = score ____ 1\n        print(f"score {____}")', ('+', 'score'),
           (('+', 'GOAL'), "<code>GOAL</code> is 10, so the terminal would say 10 after every grab."),
           (('*', 'score'), "The score starts at 0, and 0 times 1 is 0. The score would stay at 0."),
           "It is the counter from session 3, inside a gate. The two lines are inside the gate, after the lines that move the coin. The coin has jumped away, so the gate is False on the next frame, and one grab adds one point."),
         Q(TOOL2, "After the coin gate comes a second gate: has the player won? What is the test, and what does <code>playing</code> become?",
           '    if playing == 1 and score >= GOAL:\n        playing = 0\n        background = WIN\n        print(f"You win with {score} coins.")',
           '    if playing == 1 and score ____ GOAL:\n        playing = ____\n        background = WIN\n        print(f"You win with {score} coins.")', ('>=', '0'),
           (('<', '0'), "The score starts below the goal, so the game would be won on the first frame."),
           (('>=', '1'), "<code>playing</code> is already 1. Nothing would stop, and the message would print on every frame."),
           "<code>&gt;=</code> means is greater than or equal to: the score is 10 or more. The gate sets <code>playing</code> to 0, so it runs once. After that its own first test is False.",
           note="Under the coin gate, lined up with its <code>if</code>. It is a second flat gate, not inside the first one."),
         Q(TOOL2, "The window should change colour when the game is won. Which name does <code>fill</code> use now?",
           '    screen.fill(background)',
           '    screen.fill(____)', 'background',
           ('BG', "<code>BG</code> never changes, so the window would stay dark blue after a win."),
           ('WIN', "Then the window would be green from the first frame."),
           "<code>background</code> starts as <code>BG</code>, and the win gate changes it to <code>WIN</code>. The fill uses whatever colour the variable holds on that frame."),
         Q(TOOL2, "When the window closes, the terminal should say the score. The last print is replaced. What goes in the braces?",
           'print(f"final score {score}")',
           'print(f"final score {____}")', 'score',
           ('GOAL', "That prints 10 every time, even if the player grabbed two coins."),
           ('playing', "That prints 1 or 0, not the number of coins."),
           "The line is after the loop, at the left edge, so it runs once, when the window is closed."),
     ],
     "predict": "The figure touches the coin 11 times. What happens on the 11th touch?",
     "reveal": "On the 10th grab the win gate prints <code>You win with 10 coins.</code> and sets <code>playing</code> to 0. After that the coin gate's first test, <code>playing == 1</code>, is False, so the coin stays put and the score stays at 10. This is the middle exit.",
     "pick": {"right": "Nothing happens, and the score stays at 10", "wrong": [("score 11 prints", "After the win <code>playing</code> is 0, so the coin gate is False."), ("You win prints again", "<code>playing</code> is 0 after the first win, so the win gate is False too.")]},
     },
    {"title": "Tool 3: three coins in a list, and a time limit",
     "intro": "One coin is slow. Now there are three, kept in a list, and a loop asks the touching question once for each coin. There is also a time limit. The frame loop runs 60 times a second, so counting frames is counting time: when the counter reaches 30 seconds of frames and the player has not won, the window turns red and the game is over.",
     "start": TOOL2,
     "places": [('Main variables', '<code>SECONDS</code> and <code>LOSE</code>'), ('Above the loop', 'the list of three coins in place of the one coin, and <code>frame = 0</code>'), ('Inside the loop', '<code>frame = frame + 1</code>, a <code>for</code> loop around the coin gate, and the time gate'), ('Inside the loop, the drawing', 'a <code>for</code> loop around the line that draws the coin')],
     "whole": "Show the whole program",
     "code": TOOL3,
     "run": "headless", "frames": FRAMES3, "seed": SEED3, "inject": INJECT3, "fast": True,
     "steps": [
         Q(TOOL3, "The time limit is 30 seconds. It is added to the main variables. What is its name?",
           'SECONDS = 30',
           '____ = 30', 'SECONDS',
           ('seconds', "The main variables have names in capitals, so they stand out from the variables that change while the game runs."),
           ('FPS', "<code>FPS</code> is set to 60 at the end of the main variables, so this line would do nothing, and the time limit would have no name."),
           "<code>SECONDS</code> is the time limit, in seconds.",
           note="Under <code>GOAL</code>."),
         Q(TOOL3, "When time runs out, the window turns dark red. Which name holds that colour?",
           'LOSE = (156, 43, 34)',
           '____ = (156, 43, 34)', 'LOSE',
           ('WIN', "<code>WIN</code> is the green for a win. The window would turn green when time runs out."),
           ('SECONDS', "<code>SECONDS</code> already holds the time limit, 30."),
           "<code>LOSE</code> is a dark red. The time gate will fill the window with it.",
           note="Under <code>WIN</code>."),
         Q(TOOL3, "The one coin becomes a list of three coins. Each item in the list is a Rect. What goes in the blank?",
           'coins = [\n    pygame.Rect(100, 100, COIN_SIZE, COIN_SIZE),\n    pygame.Rect(300, 200, COIN_SIZE, COIN_SIZE),\n    pygame.Rect(500, 300, COIN_SIZE, COIN_SIZE),\n]',
           'coins = [\n    pygame.Rect(100, 100, COIN_SIZE, COIN_SIZE),\n    pygame.Rect(300, 200, COIN_SIZE, COIN_SIZE),\n    pygame.____(500, 300, COIN_SIZE, COIN_SIZE),\n]', 'Rect',
           ('rect', "The name has a capital R. <code>pygame.rect</code> with a small r is something else, and calling it gives an error."),
           ('draw', "<code>pygame.draw</code> draws shapes. It does not make a Rect."),
           "A list holds many values under one name, and here the values are three Rects. The list is written over five lines so each coin can be read by itself. The square brackets open on the first line and close on the last.",
           note="These five lines replace the <code>coin = pygame.Rect(...)</code> line."),
         Q(TOOL3, "Time is counted in frames. Where does the frame counter start?",
           'frame = 0',
           'frame = ____', '0',
           ('1', "Then the first frame would be counted as frame 2."),
           ('SECONDS', "That starts the counter at 30. Time would run out half a second too early."),
           "No frame has been played yet, so the counter starts at 0. The line is above the loop, so it runs once.",
           note="Under <code>background = BG</code>."),
         Q(TOOL3, "On every frame the counter goes up. What is added to it?",
           '    frame = frame + 1',
           '    frame = frame + ____', '1',
           ('0', "Adding 0 changes nothing, so the counter would stay at 0 and time would never run out."),
           ('FPS', "That adds 60 on every frame, so one second of play would count as 60 seconds."),
           "One frame is played, so the counter goes up by 1. After one second it is 60.",
           note="Inside the loop, under the gate <code>if holding == 1:</code> and its line, lined up with its <code>if</code>."),
         Q(TOOL3, "The touching question now has to be asked for every coin in the list. Which loop does that?",
           '    for coin in coins:\n        if playing == 1 and player.colliderect(coin):\n            coin.x = random.randint(0, WIDTH - COIN_SIZE)\n            coin.y = random.randint(0, HEIGHT - COIN_SIZE)\n            score = score + 1\n            print(f"score {score}")',
           '    for ____ in ____:\n        if playing == 1 and player.colliderect(coin):\n            coin.x = random.randint(0, WIDTH - COIN_SIZE)\n            coin.y = random.randint(0, HEIGHT - COIN_SIZE)\n            score = score + 1\n            print(f"score {score}")', ('coin', 'coins'),
           (('coins', 'coin'), "Those are swapped. The list is called <code>coins</code>, and the program no longer has a variable called <code>coin</code> to loop over, so Python gives a NameError."),
           (('coin', 'range(3)'), "Then <code>coin</code> would be the numbers 0, 1, and 2. A number is not a Rect, so <code>colliderect</code> gives an error."),
           "On each pass of the loop, <code>coin</code> is one of the three Rects in the list. The gate and its four lines are the same as before. Changing <code>coin.x</code> moves that Rect, and the list holds the same Rect, so the coin in the list has moved.",
           note="The gate and its four lines move one indentation level in, so they are inside the <code>for</code> loop."),
         Q(TOOL3, "After the win gate comes a third gate: has time run out? The frame counter is compared with 30 seconds of frames. How many frames is that?",
           '    if playing == 1 and frame == SECONDS * FPS:\n        playing = 0\n        background = LOSE\n        print(f"Time is up. You got {score} coins.")',
           '    if playing == 1 and frame == SECONDS ____ FPS:\n        playing = 0\n        background = ____\n        print(f"Time is up. You got {score} coins.")', ('*', 'LOSE'),
           (('+', 'LOSE'), "30 + 60 is 90 frames, which is a second and a half."),
           (('*', 'WIN'), "Then running out of time would turn the window green, the same as winning."),
           "There are 60 frames in each second, so 30 seconds is 30 times 60, which is 1800 frames. If the player has already won, <code>playing</code> is 0 and this gate stays False.",
           note="Under the win gate, lined up with its <code>if</code>."),
         Q(TOOL3, "All three coins have to be drawn on every frame. What goes in the blank?",
           '    for coin in coins:\n        pygame.draw.rect(screen, COIN, coin)',
           '    for coin in coins:\n        pygame.draw.rect(screen, COIN, ____)', 'coin',
           ('coins', "<code>coins</code> is the whole list. <code>draw.rect</code> needs one rectangle, so Python gives an error."),
           ('player', "That draws three gold squares on top of each other where the player is. The coins are never drawn."),
           "It is the same loop as the one that asks the touching question: one pass for each coin. The draw line moves one indentation level in."),
     ],
     "predict": "The figure grabs 4 coins, then stands still until the window closes on frame 1811. What are the last two lines?",
     "reveal": "Frame 1800 is 30 seconds at 60 frames a second. On that frame the time gate is True: it sets <code>playing</code> to 0, turns the window red, and prints. The last line prints when the window closes. This is the stretch exit.",
     "pick": {"right": "Time is up. You got 4 coins.   final score 4", "wrong": [("You win with 4 coins.   final score 4", "Winning needs 10 coins, the value of <code>GOAL</code>."), ("score 4   final score 4", "<code>score 4</code> prints early, on the 4th grab. On frame 1800 the time gate prints before the window closes.")]},
     },
]


# ------------------------------------------------------------------ the session

SESSION12 = {
 "num": 12,
 "slug": "session12_coin_grab",
 "title": "Coin grab",
 "subtitle": "A stick figure you pick up with a click, a coin that jumps when you touch it, and a score",
 "mon": "Mon Nov 23",
 "fri": "Fri Dec 11",
 "new": ["pygame.Rect", "left, right, top, and bottom", "the overlap test written by hand", "colliderect",
         "the mouse position", "a picture drawn inside a Rect", "a mouse click", "collidepoint", "a random spot inside the window", "a score that counts each coin once"],
 "reuse": "The window loop you copied in sessions 6 and 7, session 6's four numbers for a rectangle, session 3's counter and randint, and session 2's two tests joined with and",
 "objectives": [
   "Find a spot in a pygame window from its two numbers, (x, y), where x counts across from the left and y counts down from the top.",
   "Work out where a rectangle's right edge and bottom edge are from its x, y, width, and height.",
   "Tell whether two rectangles are touching, first by comparing their edges and then with <code>colliderect</code>.",
   "Make a stick figure that you pick up with one click and put down with the next.",
   "Make a coin jump to a random spot inside the window when the figure touches it.",
   "Keep a score that counts each coin once, and end the game with a win at ten coins.",
 ],
 "no_new_section": True,
 "teacher_standards_only": True,
 "reuse_note": "Today is the first whole game in a window, and it is short on purpose: the floor program is 51 lines of code. Chunk 4's file is 24 of them, and most of those are the window loop the students copied in sessions 6 and 7. Chunk 5 adds the six lines of the stick figure's function, chunk 6 adds twelve lines for picking the figure up and putting it down, and tool 1 adds nine. The page does not need session 11: chunk 4 says what the loop does on every frame, and why the fill and the drawing are inside it. So this session can be taught any time after session 8. Chunks 1 to 3 run in the terminal and are a few lines each, so they can be typed by everyone or run once on the projector while the room predicts. The typing starts at chunk 4. Nothing here needs the keyboard during play: a click picks the player up, the mouse moves it, and a second click puts it down.",
 "env_note": True,
 "opener": {
   "title": "Review: where things are in a pygame window",
   "minutes": 15,
   "body": "Every picture in a pygame window, and every coin in today's game, is put in its place with two numbers. This review goes over how those numbers work. Read each part together on the projector. At each check, everyone picks an answer, out loud or on paper, before anyone clicks.",
   "flow": [
     {"heading": "Two numbers for every spot",
      "teach": "A pygame window is made of <b>pixels</b>, the tiny dots that make up the screen. Every spot in the window has two numbers, written in parentheses like this: <code>(x, y)</code>. <b>x</b> is how far across the spot is from the left edge. <b>y</b> is how far down it is from the top edge. Across always comes first, then down.</p><p>The top left corner is <code>(0, 0)</code>, because it is 0 across and 0 down. Today's window is 600 wide and 400 tall, so its right edge is at x = 600 and its bottom edge is at y = 400. In the picture, the grey lines are 100 pixels apart.",
      "figure": map_figure()},
     {"q": "Where is <code>(0, 0)</code> in a pygame window?",
      "pick": {"right": "The top left corner",
               "wrong": [("The bottom left corner", "In maths class, (0, 0) is at the bottom left. In a pygame window, y counts down from the top, so 0 down is the top edge."),
                         ("The middle of the window", "0 across is the left edge, and 0 down is the top edge. The middle is (300, 200).")],
               "why": "x = 0 is the left edge and y = 0 is the top edge. The corner where those two edges meet is the top left corner."}},
     {"q": "The window is 600 wide and 400 tall. Which spot is its bottom left corner?",
      "pick": {"right": "(0, 400)",
               "wrong": [("(400, 0)", "Across comes first. (400, 0) is 400 across and 0 down, which is on the top edge."),
                         ("(0, 0)", "(0, 0) is the top left corner. The bottom edge is 400 down.")],
               "why": "The left edge is 0 across, and the bottom edge is 400 down. Across comes first, so the corner is (0, 400)."}},
     {"heading": "y goes down",
      "teach": "In maths class, y gets bigger as you go <b>up</b> the page. In a pygame window it is the other way round: y gets bigger as you go <b>down</b>. x is the same in both: it gets bigger as you go right.</p><p>So in a pygame window, adding to y moves something down, and taking away from y moves it up.",
      "figure": two_ways_figure()},
     {"q": "A dot is at <code>(200, 150)</code>. The program moves it to <code>(200, 250)</code>. Which way did the dot move?",
      "pick": {"right": "Down, by 100 pixels",
               "wrong": [("Up, by 100 pixels", "That is how y works in maths class. In a pygame window, a bigger y is further down."),
                         ("Right, by 100 pixels", "x is the first number, and it stayed at 200. Only y changed, so the dot moved up or down, not across.")],
               "why": "y went from 150 to 250, which is 100 more. A bigger y is further down the window.",
               "figure": move_figure((200, 150), (200, 250), "y + 100: down 100",
                                     "A dot moves from (200, 150) down to (200, 250)")}},
     {"q": "Dot P is at <code>(100, 300)</code> and dot Q is at <code>(100, 50)</code>. Which dot is higher on the screen?",
      "pick": {"right": "Dot Q",
               "wrong": [("Dot P", "P has the bigger y, 300, and a bigger y is further down. P is the lower dot."),
                         ("They are at the same height", "They have the same x, 100, so one is straight above the other. Their y numbers are different, so they are at different heights.")],
               "why": "Q is 50 down from the top edge, and P is 300 down. Q is closer to the top, so Q is higher.",
               "figure": spots_figure([(100, 300, "P (100, 300)", SOFT), (100, 50, "Q (100, 50)", GREEN)],
                                      "Dot Q at (100, 50) is near the top of the window. Dot P at "
                                      "(100, 300) is straight below it, near the bottom")}},
     {"q": "A coin is at <code>(300, 200)</code>. Which change moves it 50 pixels up?",
      "pick": {"right": "Change its y to 150",
               "wrong": [("Change its y to 250", "A bigger y is further down, so 250 moves the coin 50 pixels down."),
                         ("Change its x to 250", "x is across. Changing x to 250 moves the coin 50 pixels to the left.")],
               "why": "Up means a smaller y. 200 take away 50 is 150.",
               "figure": move_figure((300, 200), (300, 150), "y - 50: up 50",
                                     "A coin moves from (300, 200) up to (300, 150)")}},
     {"heading": "Finding a spot",
      "teach": "To find a spot such as <code>(450, 100)</code>, start at the top left corner. Go 450 across to the right. Then go 100 down. That is the spot.</p><p>The middle of the window is half of the width across and half of the height down. Half of 600 is 300 and half of 400 is 200, so the middle is <code>(300, 200)</code>. Today's coin starts there.",
      "figure": find_figure()},
     {"q": "Where is the middle of a window that is 600 wide and 400 tall?",
      "pick": {"right": "(300, 200)",
               "wrong": [("(200, 300)", "Across comes first. 200 across and 300 down is to the left of the middle and below it."),
                         ("(600, 400)", "That is the bottom right corner. The middle is half of each number.")],
               "why": "Half of 600 is 300, and half of 400 is 200. Across comes first, so the middle is (300, 200)."}},
     {"q": "In which part of the window is <code>(500, 80)</code>?",
      "pick": {"right": "Near the top right corner",
               "wrong": [("Near the bottom right corner", "80 down is close to the top, because the window is 400 tall. A spot near the bottom would have a y close to 400."),
                         ("Near the top left corner", "500 across is close to the right edge, because the window is 600 wide. Spots on the left have small x numbers.")],
               "why": "500 of the 600 pixels across is near the right edge, and 80 of the 400 pixels down is near the top edge.",
               "figure": spots_figure([(500, 80, "(500, 80)", GREEN)],
                                      "The spot (500, 80) is near the top right corner of the window")}},
     {"heading": "A rectangle starts at its top left corner",
      "teach": "In session 6 you drew rectangles with four numbers: <code>(x, y, width, height)</code>. The first two numbers are the spot where the rectangle's <b>top left corner</b> goes. From there the rectangle is drawn to the right by its width and down by its height.</p><p>So the right edge is x plus the width, and the bottom edge is y plus the height. Here is the tile <code>(40, 40, 200, 120)</code>.",
      "figure": tile_figure()},
     {"q": "The tile is <code>(40, 40, 200, 120)</code>. Where is its right edge?",
      "pick": {"right": "x = 240",
               "wrong": [("x = 200", "200 is the width, not where the tile ends. The tile starts at 40 across, so it ends 200 later, at 240."),
                         ("x = 160", "160 is the bottom edge: 40 down plus 120 tall. The right edge uses x and the width.")],
               "why": "The tile starts 40 across and is 200 wide. 40 + 200 is 240."}},
     {"q": "The window is 600 wide and 400 tall. Which rectangle is a strip along the bottom of the window?",
      "pick": {"right": "(0, 300, 600, 100)",
               "wrong": [("(0, 0, 600, 100)", "It starts at y = 0, so it runs along the top edge. Its bottom edge is at 100."),
                         ("(0, 400, 600, 100)", "Its top left corner is at y = 400, the bottom edge of the window, and it is drawn down from there. The whole strip is below the window, so it cannot be seen.")],
               "why": "It starts 300 down and is 100 tall, so its bottom edge is at 300 + 100, which is 400, the bottom of the window.",
               "figure": strip_figure()}},
   ],
 },
 "chunks": [
  {"title": "A Rect is four numbers with names",
   "teach": "In session 6 a rectangle was four numbers in parentheses: x, y, width, and height. <b><code>pygame.Rect</code></b> keeps those four numbers together under one name. It is written with a capital R. A Rect also works out its own edges. <code>left</code> is x, and <code>right</code> is x plus the width. <code>top</code> is y, and <code>bottom</code> is y plus the height. <code>center</code> is the pair of numbers in the middle of the rectangle; pygame spells it with <code>er</code> at the end.</p><p>This program opens no window. A Rect is only numbers, so the terminal can print them.",
   "figure": rect_figure(),
   "code": RECT,
   "run": "py",
   "predict": "What do <code>coin.right</code> and <code>coin.bottom</code> print?",
   "reveal": "300 + 30 is 330, and 200 + 30 is 230. The last line prints the middle: 15 across and 15 down from the corner, <code>(315, 215)</code>.",
   "pick": {"right": "330 and 230", "wrong": [("30 and 30", "30 is the width and the height. An edge is where the coin starts plus its size."), ("300 and 200", "Those are <code>left</code> and <code>top</code>, where the coin starts.")]}},

  {"title": "Are two rectangles touching? The test, written by hand",
   "teach": "Two rectangles are <b>touching</b> when they overlap: part of one is on top of part of the other. Checking that takes two tests. Across: each rectangle starts before the other one ends, so its <code>left</code> is less than the other one's <code>right</code>. Down: the same test with <code>top</code> and <code>bottom</code>. Both tests have to be True, and <code>and</code> joins them.</p><p>The player here is a square from 280 to 330 across and from 190 to 240 down. The coin starts below it. Then <code>coin.y = 200</code> moves the coin up, and the down test is worked out again.",
   "figure": overlap_figure(),
   "code": BY_HAND,
   "run": "py",
   "predict": "The coin is at y = 280. What does the first print say?",
   "reveal": "Across, the player is 280 to 330 and the coin is 300 to 330, so <code>across</code> is True. Down, the player ends at 240 and the coin starts at 280, so <code>down</code> is False. After <code>coin.y = 200</code> the coin is 200 to 230 down, inside 190 to 240, so the second print says touching True.",
   "pick": {"right": "across True, down False", "wrong": [("across True, down True", "At y = 280 the coin starts below 240, where the player ends. So <code>down</code> is False."), ("across False, down False", "Across, the player is 280 to 330 and the coin is 300 to 330. They overlap, so <code>across</code> is True.")]}},

  {"title": "colliderect asks the same question in one call",
   "teach": "A Rect can make that whole test itself. <b><code>player.colliderect(coin)</code></b> gives True when the two rectangles overlap and False when they do not. It is chunk 2's test, already written for you. The name is two words joined: collide, which means to bump into something, and rect.</p><p>This program asks the question three times. The first time, the coin is where chunk 2 left it, inside the player. Before the second and third times, it moves the coin by changing <code>coin.x</code>.",
   "code": COLLIDE,
   "run": "py",
   "predict": "What do the three prints say?",
   "reveal": "First True: the coin is inside the player. Then False: at x = 330 the two only share an edge, and 330 is not less than 330. Then True: at 329 the coin is one pixel inside, and one pixel is enough.",
   "pick": {"right": "True, False, True", "wrong": [("True, True, True", "At x = 330 the two only share an edge. 330 is not less than 330, so that is False."), ("True, False, False", "At 329 the coin is one pixel inside the player. One pixel is enough, so that is True.")]}},

  {"title": "A square that follows the mouse",
   "teach": "This is the first window of the day. You copied most of this file in sessions 6 and 7: the lines that open the window, and the loop that keeps it open until you close it.</p><p>The names in capitals at the top are the <b>main variables</b>. Every number the game uses gets a name there, so it can be changed in one place. <code>FPS</code> is 60, and <code>clock.tick(FPS)</code> makes the loop run 60 times a second. One pass of the loop is called a <b>frame</b>.</p><p>In sessions 6 and 7 the picture was drawn once, above the loop, because it never changed. Today the picture changes, so the drawing is inside the loop and happens on every frame. <code>screen.fill(BG)</code> paints the whole window dark blue, which covers the last frame. Then the square is drawn, and <code>pygame.display.flip()</code> puts the new picture on the screen.</p><p>Three lines are new.</p><p>The line <code>player = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)</code> makes the player, a Rect 50 across and 50 down. It is above the loop, so it runs once.</p><p>The line <code>player.center = pygame.mouse.get_pos()</code> is inside the loop, so it runs on every frame. <b><code>pygame.mouse.get_pos()</code></b> gives the position of the mouse in the window as a pair of numbers, across and then down. Storing that pair in <code>player.center</code> moves the whole square, so that its middle is on the mouse.</p><p>The line <code>pygame.draw.rect(screen, PLAYER, player)</code> draws the square. In session 6 the third thing given to <code>draw.rect</code> was four numbers in parentheses. A Rect works in the same place.</p><p>The last print runs when you close the window.",
   "code": MOUSE,
   "run": "headless",
   "frames": 6,
   "inject": [[2, "MOUSE", 300, 200]],
   "predict": "The mouse is at (300, 200). What are <code>left</code> and <code>top</code>?",
   "reveal": "Half of 50 is 25, so the left edge is 25 to the left of the mouse and the top edge is 25 above it. The run on this page was given the mouse position (300, 200). Yours depends on where your mouse is. If your square stays in the top left corner, the mouse is outside the window.",
   "pick": {"right": "275 and 175", "wrong": [("300 and 200", "That is the centre. The middle is on the mouse, so the edges are 25 away."), ("250 and 150", "That is 50 away, the whole width. Each edge is half of 50 away from the middle.")]}},

  {"title": "The player becomes a stick figure",
   "teach": "The white square is the player's Rect, drawn so you can see it. The game does not have to draw the Rect. It can draw any picture in the same place, and the Rect goes on doing its job: it follows the mouse, and later it is what touches the coin.</p><p>The new function, <code>draw_player</code>, draws a stick figure: a circle for the head, a line for the body, a thin rectangle for the arms, and two lines for the legs. It is a function that draws, like <code>tile</code> in session 6. Its two parameters are <code>x</code>, the middle of the player across, and <code>y</code>, the top of the player. Every number in it is measured from those two. <code>pygame.draw.circle</code> takes the middle of the circle and then its radius, which is how far the edge is from the middle. <code>pygame.draw.line</code> takes where the line starts and where it ends. The 3 at the end of the circle and of each line is how thick it is drawn. The arms are a rectangle 40 wide and 3 tall, which looks like a line lying flat.</p><p>Two things change in chunk 4's file. The function goes near the top, after the main variables and before <code>pygame.init()</code>, with an empty line above and below. Inside the loop, the line <code>pygame.draw.rect(screen, PLAYER, player)</code> is replaced by the call <code>draw_player(player.centerx, player.top)</code>. <code>player.centerx</code> is the first number of <code>player.center</code>.</p><p>The figure is 50 tall, from the top of the head to the feet, and its arms are 40 across, so it fits inside the Rect. A coin is grabbed when it touches the Rect, not when it touches a line of the figure.",
   "code": STICK,
   "places": [("Between the main variables and <code>pygame.init()</code>", "the function <code>draw_player</code>"),
             ("Inside the loop", "<code>draw_player(player.centerx, player.top)</code> in place of the line that drew the square")],
   "run": "headless",
   "frames": 6,
   "inject": [[2, "MOUSE", 300, 200]],
   "predict": "The mouse is at (300, 200). Where is the middle of the head?",
   "reveal": "<code>x</code> is 300 and <code>y</code> is 175, the top of the Rect. The head is drawn at <code>(x, y + 10)</code>, and 175 + 10 is 185. The feet are at <code>y + 50</code>, 225, the bottom of the Rect.",
   "pick": {"right": "(300, 185)", "wrong": [("(300, 200)", "That is the mouse, the middle of the Rect. The head is near the top."), ("(300, 210)", "In the function, <code>y</code> is the top of the Rect, 175, not the mouse's 200.")]}},

  {"title": "Click to pick it up, click to put it down",
   "teach": "Right now the figure follows the mouse all the time, so the mouse cannot do anything else. In this chunk the first click on the figure picks it up, and it follows the mouse. The next click, anywhere, puts it down where it is. While the figure is down, the mouse is free to click on something else in the window.</p><p>A click is an <b>event</b>, like closing the window. When the mouse button is pressed, <code>pygame.event.get()</code> gives an event whose type is <code>pygame.MOUSEBUTTONDOWN</code>. Inside the event loop the program only writes down that there was a click: <code>click = 1</code>. The line <code>click = 0</code> at the top of the frame loop puts it back to 0 on every frame, so one click counts on one frame only.</p><p><code>holding</code> says whether the figure is picked up: 1 for yes, 0 for no. It starts at 0, above the loop.</p><p><b><code>player.collidepoint(mouse)</code></b> is True when the spot <code>mouse</code> is inside the player's Rect. So a click picks the figure up only if it lands on the figure.</p><p>The player now starts with its top left corner at (75, 175), so its middle is at (100, 200), where you can see it and click it. The last print says where the player is and whether it is held.",
   "code": CLICK,
   "start": STICK,
   "places": [("Above the loop", "the player's new starting spot, and <code>holding = 0</code>"),
             ("The first line inside the loop", "<code>click = 0</code>"),
             ("Inside the event loop", "a gate that notes a click"),
             ("Where the player moved", "<code>mouse</code>, the two click gates, and the gate that moves the player while it is held"),
             ("After the loop", "the last print")],
   "steps": [
       Q(CLICK, "The figure has to start where you can see it and click it. Its top left corner goes at (75, 175). What are the first two numbers?",
         'player = pygame.Rect(75, 175, PLAYER_SIZE, PLAYER_SIZE)',
         'player = pygame.Rect(____, ____, PLAYER_SIZE, PLAYER_SIZE)', ('75', '175'),
         (('100', '200'), "That puts the top left corner at (100, 200). The first two numbers are the corner, not the middle."),
         (('175', '75'), "Across comes first. That corner is 175 across and 75 down."),
         "A Rect's first two numbers are its top left corner. The player is 50 wide and 50 tall, so its middle is 25 further across and 25 further down: (100, 200).",
         note="This line replaces <code>player = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)</code>."),
       Q(CLICK, "The program needs to know, on every frame, whether the figure is picked up. Where does <code>holding</code> start?",
         'holding = 0',
         'holding = ____', '0',
         ('1', "Then the figure would follow the mouse from the first frame, before anyone clicks it."),
         ('"no"', "With quote marks it is text. The gates below compare <code>holding</code> with the numbers 1 and 0."),
         "Nobody has clicked yet, so the figure is not picked up. The line is above the frame loop, so it runs once.",
         note="Under the <code>player</code> line."),
       Q(CLICK, "Each frame starts with no click yet. Which line goes first inside the frame loop?",
         '    click = 0',
         '    click = ____', '0',
         ('1', "Then every frame would count as a click, and the figure would be picked up and put down over and over."),
         ('holding', "That copies <code>holding</code> into <code>click</code>. <code>click</code> is about a click on this frame, not about holding."),
         "<code>click</code> goes back to 0 at the start of every frame, so one click counts on one frame only.",
         note="The first line under <code>while running:</code>, one indentation level in."),
       Q(CLICK, "A click is an event. Which event type means the mouse button was pressed?",
         '        if event.type == pygame.MOUSEBUTTONDOWN:\n            click = 1',
         '        if event.type == pygame.____:\n            click = 1', 'MOUSEBUTTONDOWN',
         ('QUIT', "<code>QUIT</code> is closing the window. That gate is already the one above."),
         ('mouse.get_pos()', "<code>get_pos</code> gives where the mouse is, not whether it was clicked. It is not an event type."),
         "Pressing the mouse button makes one <code>MOUSEBUTTONDOWN</code> event. The gate writes down that there was a click this frame.",
         note="Inside the <code>for event</code> loop, under the QUIT gate and lined up with its <code>if</code>."),
       Q(CLICK, "The gates below need to know where the mouse is. Which line stores it?",
         '    mouse = pygame.mouse.get_pos()',
         '    mouse = pygame.mouse.____()', 'get_pos',
         ('center', "<code>center</code> belongs to a Rect, like <code>player.center</code>. Where the mouse is comes from <code>get_pos</code>."),
         ('MOUSEBUTTONDOWN', "That is the type of a click event. It does not say where the mouse is."),
         "<code>get_pos</code> gives where the mouse is, as (x, y). The player no longer moves here; it moves only in the gate further down.",
         note="This line replaces <code>player.center = pygame.mouse.get_pos()</code>, in the same place."),
       Q(CLICK, "The figure is held and the player clicks. The figure is put down. Which two tests go in this gate?",
         '    if click == 1 and holding == 1:\n        holding = 0\n        print("put down")',
         '    if click == 1 and holding == ____:\n        holding = ____\n        print("put down")', ('1', '0'),
         (('0', '1'), "Those are swapped. That gate would pick the figure up, with a click anywhere in the window."),
         (('1', '1'), "<code>holding</code> is already 1. Nothing would change, so the figure could never be put down."),
         "When there is a click and the figure is held, <code>holding</code> becomes 0. The terminal says what happened.",
         note="Under the line <code>mouse = pygame.mouse.get_pos()</code>."),
       Q(CLICK, "The figure is down and the player clicks. The click should pick it up only if it lands on the figure. Which word starts this gate?",
         '    elif click == 1 and player.collidepoint(mouse):\n        holding = 1\n        print("picked up")',
         '    ____ click == 1 and player.collidepoint(mouse):\n        holding = 1\n        print("picked up")', 'elif',
         ('if', "With a second <code>if</code>, the click that puts the figure down is also on the figure. The gate above sets <code>holding</code> to 0, then this gate sets it straight back to 1 on the same frame, so the figure can never be put down."),
         ('else', "<code>else</code> takes no test. Every frame without a click would pick the figure up."),
         "<code>elif</code> runs only when the gate above it was False. So one click does one thing: it puts the figure down, or it picks it up, never both. <code>collidepoint(mouse)</code> is True when the mouse is inside the player's Rect."),
       Q(CLICK, "The figure follows the mouse only while it is held. What goes in the blank?",
         '    if holding == 1:\n        player.center = mouse',
         '    if holding == ____:\n        player.center = mouse', '1',
         ('0', "Then the figure would follow the mouse while it is put down, and stop while it is held."),
         ('click', "<code>click</code> is 1 on one frame only, so the figure would jump to the mouse once and stop."),
         "<code>player.center = mouse</code> is the line from chunk 4, now inside a gate. While <code>holding</code> is 0 the line does not run, so the figure stays where it was put down."),
       Q(CLICK, "The last print should say whether the figure is held when the window closes. What goes in the braces?",
         'print(f"centre {player.center}, holding {holding}")',
         'print(f"centre {player.center}, holding {____}")', 'holding',
         ('click', "<code>click</code> only says whether there was a click on the last frame."),
         ('mouse', "That prints where the mouse was, not whether the figure is held."),
         "<code>holding</code> is 1 if the figure is held and 0 if it is put down.",
         note="This line replaces the last print, after the loop at the left edge."),
   ],
   "run": "headless",
   "frames": 10,
   "inject": [[2, "CLICK", 100, 200], [4, "MOUSE", 400, 300], [6, "CLICK", 400, 300], [8, "MOUSE", 500, 100]],
   "predict": "Click the figure, move to (400, 300), click, then move to (500, 100). Where does the figure end up?",
   "reveal": "The first click is on the figure, so it is picked up and follows the mouse to (400, 300). The second click puts it down there. After that <code>holding</code> is 0, so it stays when the mouse moves on. The terminal says <code>picked up</code>, then <code>put down</code>.",
   "pick": {"right": "(400, 300)", "wrong": [("(500, 100)", "The second click put the figure down. After that <code>holding</code> is 0, so it does not follow the mouse."), ("(100, 200)", "The first click was on the figure, so it was picked up and followed the mouse.")]}},
 ],
 "hinge": {"q": "One second of a frame loop, without the window. <code>touching</code> stays True on all 60 frames. What does it print?",
           "code": HINGE,
           "run": "py",
           "code_a": '    if touching:\n        score = score + 1\n        touching = False',
           "a": "The gate is True on every frame, so the score goes up 60 times in one second. To make it print 1, add <code>touching = False</code> inside the gate, as below. In the game, moving the coin does that job: once the coin has jumped away, <code>player.colliderect(coin)</code> is False on the next frame.",
           "pick": {"right": "60", "wrong": [("1", "Nothing in the gate makes <code>touching</code> False, so the gate is True on all 60 frames."), ("0", "<code>touching</code> is True, so the gate runs and adds 1.")]}},
 "brief": {
   "title": "Build: coin grab",
   "minutes": 30,
   "intro": "You are making a small game called coin grab. You click the stick figure to pick it up, and it follows the mouse until you click again. A gold coin sits in the window. When the figure touches the coin, the coin jumps to a new spot picked at random, and the terminal counts it. Ten coins wins the game. The build is one program, written in three tools. Each tool starts from the program the tool before it finished.",
   "tools": TOOLS12,
   "steps": [
     "Start from chunk 6's file, <code>Jonathan_session12.py</code> with your first name in place of Jonathan: the stick figure you pick up with a click.",
     "Add a coin, and make it jump to a random spot when the player touches it.",
     "Add a score that goes up by 1 for each coin, printed in the terminal.",
     "End the game at ten coins: the window turns green and the coin stops jumping.",
     "Put three coins in a list, and add a 30 second time limit that turns the window red.",
   ],
   "expected_got": [
     ["Clicking the stick figure picks it up, and it follows the mouse with the pointer in the middle of its body", ""],
     ["A second click puts the figure down, and it stays there when the mouse moves", ""],
     ["Touching the coin makes it jump, and the whole coin is inside the window every time", ""],
     ["One coin adds 1 to the score, not 60 a second", ""],
     ["After ten coins the window is green, and touching a coin does nothing", ""],
     ["With three coins, any one of them can be grabbed", ""],
     ["After 30 seconds without a win the window is red and the terminal says how many coins you got", ""],
   ],
 },
 "exits": {
   "floor": "Tool 1: a click picks up the stick figure and the next click puts it down, and the coin jumps to a random spot when the figure touches it.",
   "middle": "Tool 2: the score is printed in the terminal, and at ten coins the window turns green and the game stops.",
   "stretch": "Tool 3: three coins in a list, and a 30 second time limit that turns the window red.",
 },
 "extension": {
   "title": "Give the jump a name",
   "intro": "<p>The two <code>randint</code> lines move a coin to a random spot. A function can hold them, so the game can move a coin from more than one place. Then every game can start with its coins in different spots.</p>",
   "cards": [
     {"title": "move_coin changes the Rect it is given",
      "teach": "This function has one parameter, <code>coin</code>, and no <code>return</code> line. It does not work out a value. It changes the Rect that the call gives it. The program prints where the coin is, calls the function, and prints where the coin is again. The last line prints what the function returns.",
      "code": MOVE_COIN,
      "run": "py",
      "seed": 2,
      "predict": "What happens to the coin, and what does the last line print?",
      "reveal": "A function with no <code>return</code> line returns None, as in session 5. The coin moves: the first print says 300 200 and the second says 57 46. The last line moves it once more, then prints None. Your numbers will be different.",
      "pick": {"right": "It moves, and the last line prints None", "wrong": [("It moves, and the last line prints the new spot", "<code>move_coin</code> has no <code>return</code> line, so it returns None."), ("It does not move, and the last line prints None", "The function changes the Rect it is given, so the coin moves. The second print shows a new spot.")]}},
   ],
   "steps": [
     "Put <code>move_coin</code> in your tool 3 file. Functions go near the top, after the main variables and before <code>pygame.init()</code>, with an empty line above and below.",
     "Inside the coin gate, replace the two <code>randint</code> lines with one call: <code>move_coin(coin)</code>.",
     "Under the <code>coins</code> list, add a loop that calls <code>move_coin(coin)</code> once for each coin, so every game starts with the coins in new spots.",
     "Change one main variable, <code>COIN_SIZE</code>, <code>GOAL</code>, or <code>SECONDS</code>, to make the game harder. One change per run.",
   ],
   "checks": [
     "The game plays the same as before the function was added",
     "Run the game twice: the three coins start in different spots each time",
     "The variable you changed makes the game harder, and you can say why",
   ],
 },
 "ledger": "Stamp 12: <code>pygame.Rect(x, y, w, h)</code> has <code>left</code>, <code>right</code>, <code>top</code>, <code>bottom</code>, and <code>center</code>; <code>a.colliderect(b)</code> is True when two rectangles overlap; <code>pygame.mouse.get_pos()</code> is where the mouse is; <code>a.collidepoint(spot)</code> is True when the spot is inside the rectangle; a click is a <code>MOUSEBUTTONDOWN</code> event; move the coin inside the gate, so one grab counts once.",
 "teacher": {
   "timing": [
     "0:00 opener, a review of where things are in the window, 15 min (nine checks; everyone picks before you click)",
     "0:15 chunk 1, a Rect and its edges, 5 min (the opener already did x + width)",
     "0:20 chunk 2, the overlap test by hand, 10 min (project the figure; this is the mathematics of the day)",
     "0:30 chunk 3, colliderect, 5 min",
     "0:35 chunk 4, the mouse, 12 min (the first window file; most of the typing is here)",
     "0:47 chunk 5, the stick figure, 8 min",
     "0:55 chunk 6, click to pick up and put down, 7 min",
     "1:02 hinge question, 3 min",
     "1:05 build, tools 1 and 2, 20 min (tool 3 is for students who are ahead)",
     "1:25 exits, ledger stamp, 5 min",
   ],
   "misconceptions": [
     ["Types <code>pygame.rect</code> with a small r, or <code>Rect</code> without <code>pygame.</code> in front.",
      "Read the last line of the error together. The capital R is the difference between the Rect that holds numbers and <code>pygame.draw.rect</code>, which draws."],
     ["Puts the <code>coin = pygame.Rect(...)</code> line inside the frame loop. The coin flickers back to 300, 200.",
      "Ask how many times that line should run. Once, so it goes above the loop."],
     ["Puts <code>score = 0</code> inside the loop and the score never passes 1.",
      "It is session 3's counter. The starting value goes above the loop."],
     ["Expects two rectangles that share an edge to count as touching.",
      "Go back to chunk 3's second print. 330 is not less than 330. One pixel of overlap is needed."],
     ["Runs the program and reports that the player will not move.",
      "From chunk 6 on, the figure moves only after a click on it. If it was clicked, the mouse may be outside the window, or the window may be behind VS Code. <code>get_pos</code> only follows the mouse while it is over the window."],
     ["Writes the second gate of chunk 6 as <code>if</code>, not <code>elif</code>. The figure can be picked up but never put down.",
      "The click that puts it down is on the figure, so with a second <code>if</code> the next gate picks it straight back up on the same frame. With <code>elif</code>, only one of the two gates runs for a click."],
     ["Draws the coin above <code>screen.fill</code> and the coin never appears.",
      "The fill paints over everything drawn before it on that frame. Whatever is drawn last is on top."],
   ],
   "standards": ["NY-5.G.1", "NY-6.NS.8", "NY-6.EE.5"],
   "routing": "Chunks 1 to 3 need no window. If time is short, run them once on the projector and have the room predict out loud, then go to chunk 4, where everyone types. Tool 1 is the floor exit and it adds nine lines to chunk 6's file. If chunk 5 has to be skipped, the build works the same with chunk 4's white square as the player: the only difference is the one line that draws it. If chunk 6 has to be skipped, the build also works from chunk 5's file, with the figure following the mouse all the time; put the coin lines under <code>player.center = pygame.mouse.get_pos()</code>. Tool 2 is the middle exit. Every tool has its finished program behind a button, so a student who falls behind can read it and run it. The extension is for a student who finishes tool 3. Nothing survives on the machines, so the game cannot be carried into session 13; session 13 starts from its own file.",
 },
}
