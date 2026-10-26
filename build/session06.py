# Session 6: a Mondrian made of rectangles. Added October 2026 between the functions
# session and the angles session, so the first pygame window of the term is one
# function, tile, called over and over with different numbers.

SETUP = '''import pygame

WIDTH = 640
HEIGHT = 480
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 38, 38)
BLUE = (37, 99, 235)
YELLOW = (252, 211, 77)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)
'''

LOOP = '''
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

# the whole chunk 1 program: setup, an empty drawing section, the loop
WINDOW = SETUP + '\n# ---- your drawing, done once ----\n' + LOOP

TILE_DEF = '''def tile(color, x, y, w, h):
    pygame.draw.rect(canvas, color, (x, y, w, h))
    pygame.draw.rect(canvas, BLACK, (x, y, w, h), 10)'''

MONDRIAN_CALLS = '''tile(RED, 0, 0, 400, 300)
tile(WHITE, 400, 0, 240, 300)
tile(BLUE, 0, 300, 160, 180)
tile(WHITE, 160, 300, 240, 180)
tile(YELLOW, 400, 300, 240, 100)
tile(WHITE, 400, 400, 240, 80)'''

WHERE_DRAW = ('Add these lines to the file you made in chunk 1, under the comment '
              '<code># ---- your drawing, done once ----</code>. That is after '
              '<code>canvas.fill(WHITE)</code>, so the canvas exists before you draw on it, '
              'and before <code>while running:</code>, because the loop only shows what was '
              'drawn before it started. Then run the whole file.')

WHERE_TILE = ('Two places in the file you made in chunk 1. The three lines of the function go '
              'near the top, after the colour lines and before <code>pygame.init()</code>, with '
              'an empty line on each side. The function uses <code>canvas</code>, which is '
              'made further down, and that is fine: a <code>def</code> does not run anything. '
              'The function only runs when it is called, and by then the canvas exists. The '
              'calls go under the comment <code># ---- your drawing, done once ----</code>, '
              'in place of chunk 3\'s two lines. Then run the whole file.')


def window_figure():
    """The 640 by 480 window at half size with one tile, and the four numbers that place it."""
    return ('<svg viewBox="0 0 660 300" width="100%" role="img" aria-label="A 640 by 480 '
            'window drawn at half size, with a red tile 200 wide and 120 tall whose top left '
            'corner is at 40, 40; x grows across and y grows down from the top left corner" '
            'style="max-width:660px;display:block;margin:0 0 16px;font-family:JetBrains Mono,'
            'monospace;font-size:13px">'
            # the window, 320 by 240, so every window number is halved on the page
            '<rect x="60" y="40" width="320" height="240" fill="#FFFFFF" stroke="#D3CBB8" stroke-width="2"/>'
            '<text x="60" y="296" fill="#4A4D53">the window: 640 across, 480 down</text>'
            # axes drawn outside the window
            '<circle cx="60" cy="40" r="4" fill="#17181B"/>'
            '<text x="68" y="18" fill="#17181B" font-weight="700">(0, 0) top left</text>'
            '<line x1="60" y1="30" x2="150" y2="30" stroke="#0E4D52" stroke-width="3"/>'
            '<polygon points="150,25 160,30 150,35" fill="#0E4D52"/>'
            '<text x="168" y="34" fill="#0E4D52" font-weight="700">x grows across</text>'
            '<line x1="48" y1="40" x2="48" y2="130" stroke="#0E4D52" stroke-width="3"/>'
            '<polygon points="43,130 48,140 53,130" fill="#0E4D52"/>'
            '<text x="20" y="160" fill="#0E4D52" font-weight="700" transform="rotate(-90 20 160)">y grows down</text>'
            # the tile: window (40, 40, 200, 120) is page (80, 60, 100, 60)
            '<rect x="80" y="60" width="100" height="60" fill="#DC2626" stroke="#17181B" stroke-width="5"/>'
            '<circle cx="80" cy="60" r="4" fill="#17181B"/>'
            '<text x="90" y="55" fill="#17181B" font-weight="700">starts at x = 40, y = 40</text>'
            '<line x1="80" y1="132" x2="180" y2="132" stroke="#1D5B39" stroke-width="3"/>'
            '<text x="100" y="150" fill="#1D5B39" font-weight="700">w = 200</text>'
            '<line x1="192" y1="60" x2="192" y2="120" stroke="#9C2B22" stroke-width="3"/>'
            '<text x="200" y="94" fill="#9C2B22" font-weight="700">h = 120</text>'
            '<text x="80" y="200" fill="#1D5B39" font-weight="700">right edge: x + w = 240</text>'
            '<text x="80" y="224" fill="#9C2B22" font-weight="700">bottom edge: y + h = 160</text>'
            # the key
            '<text x="410" y="70" fill="#17181B" font-weight="700">(x, y, w, h)</text>'
            '<text x="410" y="100" fill="#4A4D53">x  how far across it starts</text>'
            '<text x="410" y="122" fill="#4A4D53">y  how far down it starts</text>'
            '<text x="410" y="144" fill="#4A4D53">w  how wide it is</text>'
            '<text x="410" y="166" fill="#4A4D53">h  how tall it is</text>'
            '<text x="410" y="206" fill="#4A4D53">the picture is half size:</text>'
            '<text x="410" y="228" fill="#4A4D53">every number is twice what</text>'
            '<text x="410" y="250" fill="#4A4D53">you see here</text>'
            '</svg>')


def plan_figure():
    """The six-tile plan from chunk 5, drawn at three quarters size with its numbers."""
    tiles = [
        ("#DC2626", 0, 0, 400, 300, "RED", "#FFFFFF"),
        ("#FFFFFF", 400, 0, 240, 300, "WHITE", "#17181B"),
        ("#2563EB", 0, 300, 160, 180, "BLUE", "#FFFFFF"),
        ("#FFFFFF", 160, 300, 240, 180, "WHITE", "#17181B"),
        ("#FCD34D", 400, 300, 240, 100, "YELLOW", "#17181B"),
        ("#FFFFFF", 400, 400, 240, 80, "WHITE", "#17181B"),
    ]
    k = 0.75
    out = ['<svg viewBox="0 0 520 400" width="100%" role="img" aria-label="The plan for the '
           'six tiles: red 400 by 300 at the top left, white 240 by 300 at the top right, '
           'blue 160 by 180 at the bottom left, white 240 by 180 beside it, yellow 240 by 100 '
           'and white 240 by 80 stacked at the bottom right" '
           'style="max-width:520px;display:block;margin:0 0 16px;font-family:JetBrains Mono,'
           'monospace;font-size:12px">']
    for fill, x, y, w, h, name, ink in tiles:
        out.append('<rect x="%g" y="%g" width="%g" height="%g" fill="%s" stroke="#17181B" '
                   'stroke-width="6"/>' % (20 + x * k, 20 + y * k, w * k, h * k, fill))
        out.append('<text x="%g" y="%g" fill="%s" font-weight="700">%s</text>'
                   % (20 + x * k + 10, 20 + y * k + 22, ink, name))
        out.append('<text x="%g" y="%g" fill="%s" font-size="11">%d, %d, %d, %d</text>'
                   % (20 + x * k + 6, 20 + y * k + 40, ink, x, y, w, h))
    out.append('<text x="20" y="14" fill="#4A4D53">each tile: x, y, w, h</text>')
    out.append('<text x="20" y="392" fill="#4A4D53">0 and 400 and 640 across; 0 and 300 and 480 down</text>')
    out.append('</svg>')
    return "".join(out)


SESSION06 = {
 "num": 6,
 "slug": "session06_mondrian_rectangles",
 "title": "A Mondrian made of rectangles",
 "subtitle": "One function that draws a tile, called again and again with your own numbers",
 "mon": "Mon Nov 2",
 "fri": "Fri Oct 23",
 "new": ["a window", "a colour as three numbers", "pygame.draw.rect", "x, y, width, height", "a border with a thickness", "a function that draws", "tiles that touch", "a picture made by calling one function many times"],
 "reuse": "Session 5: def, a parameter, an argument, and a function called more than once",
 "reuse_note": "Piet Mondrian was a Dutch painter who, about a hundred years ago, made paintings out of nothing but rectangles: red, blue, yellow, and white, with thick black lines between them. Today the class makes one in a window. The function that draws one tile is three lines long and the students write it one line at a time, with the hints opening one inside the next. After that they copy the calls and change the numbers. Every number a student changes moves something they can see, which is the point of the session. The window code at the top and bottom of the file is copied, not taught; session 11 takes it apart. Nobody needs to understand the loop today.",
 "env_note": True,
 "opener": {
   "title": "Retrieval: a function with parameters",
   "minutes": 10,
   "body": "Paper first. Then open the editor, make <code>Jonathan_session06.py</code> with your own first name in place of Jonathan, and check the first answer.",
   "questions": [
     {"q": "Write a function called <code>greet</code> with one parameter, <code>name</code>, that prints Welcome and the name. Then call it twice with two different names.",
      "code_a": 'def greet(name):\n    print(f"Welcome, {name}.")\n\ngreet("Ada")\ngreet("Grace")',
      "a": "The <code>def</code> line, the print indented under it, then two calls at the left edge. <code>name</code> is the parameter, written once on the <code>def</code> line. <code>\"Ada\"</code> and <code>\"Grace\"</code> are the arguments, one per call. Today's function has five parameters, and it gets called six times."},
     {"q": "In <code>def area(w, h):</code> and the call <code>area(3, 4)</code>, which words are parameters, which values are arguments, and what is <code>h</code> while that call runs?",
      "a": "<code>w</code> and <code>h</code> are the parameters. 3 and 4 are the arguments. The arguments fill the parameters in order, so <code>w</code> is 3 and <code>h</code> is 4 for that one call. Order is the whole thing: <code>area(4, 3)</code> gives the same number, but today <code>tile(RED, 40, 40, 200, 120)</code> and <code>tile(RED, 40, 40, 120, 200)</code> draw two different shapes."},
   ],
 },
 "chunks": [
  {"title": "A white window",
   "teach": "Every program this term has put its words in the terminal. This one opens a window instead, and the words stay in the terminal. Type it all. The lines at the top set the window up and the lines at the bottom keep it open until you close it; both are copied, not studied. Session 11 takes the loop apart. Today the only part that matters is the empty space under the comment in the middle. That is where the drawing goes.</p><p>Every colour is three numbers in parentheses: how much red, how much green, and how much blue, each from 0 to 255. All three at 255 is white and all three at 0 is black. <code>canvas</code> is a blank picture the size of the window, kept in memory, and <code>canvas.fill(WHITE)</code> paints all of it white. The loop at the bottom copies the canvas onto the window sixty times a second.",
   "code": WINDOW,
   "run": "headless",
   "frames": 5,
   "predict": "The program has no print in it. When you run it, what shows up in the terminal, and what shows up on the screen?",
   "reveal": "The terminal shows only pygame's two greeting lines, and a white window opens. It can open behind VS Code, so check the taskbar before deciding nothing happened. Close it with its own close button. Words go in the terminal and visuals go in the window, and that split holds all term."},

  {"title": "One rectangle",
   "teach": "<code>pygame.draw.rect</code> draws a rectangle on the canvas. It takes the canvas, the colour, and then four numbers in parentheses: <code>x</code>, how far across the rectangle starts; <code>y</code>, how far down it starts; <code>w</code>, how wide it is; and <code>h</code>, how tall it is. The top left corner of the window is 0, 0, and <code>y</code> counts down from the top, not up from the bottom. That is the one way a window is unlike graph paper.</p><p>The print is a probe. It works out where the right edge lands, so you can check it against what you see.",
   "figure": window_figure(),
   "prefix": SETUP,
   "where": WHERE_DRAW,
   "code": 'pygame.draw.rect(canvas, RED, (40, 40, 200, 120))\nprint(f"the red tile runs from x = 40 to x = {40 + 200}")',
   "run": "headless",
   "frames": 3,
   "predict": "The tile starts 40 across and is 200 wide. Where is its right edge? And if you changed the 40 for <code>y</code> to 300, would the tile move down the window or up it?",
   "hint": ["The right edge is where the tile starts plus how wide it is.", "Larger <code>y</code> numbers are lower on the screen, because <code>y</code> counts down from the top."],
   "reveal": "At 240, because 40 plus 200 is 240, and the probe prints the same number. A <code>y</code> of 300 moves the tile down, to a strip that starts 300 from the top and ends at 420. The width and height do not say where the tile ends; they say how big it is. To know where it ends, add."},

  {"title": "A black border",
   "teach": "A Mondrian has thick black lines between the colours. <code>pygame.draw.rect</code> draws a border instead of a filled shape when you give it a fifth value: the thickness of the line, in pixels. Leave it out and the rectangle is filled.</p><p>Draw the red fill first and the black border second, with the same four numbers. Later drawing goes on top of earlier drawing, the way a later coat of paint covers an earlier one.",
   "prefix": SETUP,
   "where": WHERE_DRAW,
   "code": 'pygame.draw.rect(canvas, RED, (40, 40, 200, 120))\npygame.draw.rect(canvas, BLACK, (40, 40, 200, 120), 10)\nprint("one red tile with a black border")',
   "run": "headless",
   "frames": 3,
   "predict": "The same four numbers appear on both lines. What does the 10 on the second line do? And if you swapped the two lines, what would you see?",
   "hint": ["Try it. Change the 10 to 30, run it, then take it out altogether and run it again."],
   "reveal": "The 10 is the thickness of the border, so the black line is ten pixels wide. Take it out and the black rectangle is filled, so it covers the red one completely. Swap the two lines and the red fill is drawn on top of the border and covers it, so the border disappears except where it sticks out. Fill first, border second."},

  {"title": "A function that draws one tile",
   "teach": "Every tile needs those same two lines with the same four numbers twice. Six tiles would be twelve lines, and a change to one number would have to be made twice. So the two lines go in a function. Session 5's <code>greet</code> had one parameter. This one has five: the colour and the four numbers. Each line is a question for the room before it goes on the screen.",
   "prefix": SETUP,
   "where": WHERE_TILE,
   "start": 'pygame.draw.rect(canvas, RED, (40, 40, 200, 120))\npygame.draw.rect(canvas, BLACK, (40, 40, 200, 120), 10)',
   "steps": [
     {"label": "Line 1",
      "q": "The function is called <code>tile</code>. It needs to be told a colour and the four numbers. Which line starts it?",
      "hints": ["A function starts with <code>def</code>, its name, parentheses, and a colon. The blanks the caller fills in go inside the parentheses, with commas between them.",
                "Five blanks: the colour first, then <code>x</code>, <code>y</code>, <code>w</code>, <code>h</code> in the same order as chunk 2.",
                {"text": "Fill the blank.", "code": 'def tile(____, x, y, w, h):'}],
      "line": 'def tile(color, x, y, w, h):'},
     {"label": "Line 2",
      "q": "What is the first thing the function draws, and how far in is the line indented?",
      "hints": ["Chunk 3's first line, the filled rectangle, indented four spaces so it belongs to the <code>def</code>.",
                "In chunk 3 the colour was <code>RED</code> and the numbers were written in. Here they come from the parameters, so the line uses the parameter names instead.",
                {"text": "Fill the blank.", "code": '    pygame.draw.rect(canvas, color, (____, y, w, h))'}],
      "line": '    pygame.draw.rect(canvas, color, (x, y, w, h))'},
     {"label": "Line 3",
      "q": "What does the function draw second?",
      "hints": ["Chunk 3's second line, the border. The border is always black, so <code>BLACK</code> stays as it is. The four numbers come from the parameters.",
                {"text": "Fill the blank.", "code": '    pygame.draw.rect(canvas, BLACK, (x, y, w, h), ____)'}],
      "line": '    pygame.draw.rect(canvas, BLACK, (x, y, w, h), 10)'},
     {"label": "Line 5",
      "q": "The function is written and draws nothing yet. Which line draws the red tile from chunk 3 with it?",
      "hints": ["A call: the name, then parentheses with five arguments in the order of the parameters.",
                "The first argument is the colour. The other four are chunk 3's numbers.",
                {"text": "Fill the blank.", "code": 'tile(RED, 40, 40, ____, 120)'}],
      "line": 'tile(RED, 40, 40, 200, 120)',
      "note": "At the left edge, under the drawing comment, with an empty line between the function and the call."},
     {"label": "Line 6",
      "q": "A blue tile, the same height, right next to the red one with no gap. Where does it start?",
      "hints": ["It starts where the red tile ends. Chunk 2 worked out where that is.",
                "The red tile runs from 40 to 240, so the blue one starts at <code>x = 240</code>. Same <code>y</code>, same height, any width you like.",
                {"text": "Fill the blank.", "code": 'tile(BLUE, ____, 40, 160, 120)'}],
      "line": 'tile(BLUE, 240, 40, 160, 120)'},
   ],
   "code": TILE_DEF + '\n\ntile(RED, 40, 40, 200, 120)\ntile(BLUE, 240, 40, 160, 120)\nprint(f"the blue tile starts at x = {40 + 200}, where the red one ends")',
   "run": "headless",
   "frames": 3,
   "predict": "Two calls to <code>tile</code>. How many rectangles get drawn, and why is the black line between the red and the blue thicker than the line round the outside?",
   "reveal": "Four: each call draws a fill and then a border, so two calls draw two fills and two borders. A border is drawn inside its own tile. The red tile's right border ends at x = 240 and the blue tile's left border starts there, so the two borders sit side by side and join into one line twice as thick, 20 pixels instead of 10. Every line between two tiles in a Mondrian comes out that way, and the outside edge of the picture stays thin. That is why tiles that touch share a number."},

  {"title": "A whole Mondrian",
   "teach": "Six tiles that fill the window exactly. The plan is on the figure: the window is 640 across and 480 down, and the tiles are cut by one line across at 300 and one line down at 400, with the bottom right cut again at 400. Each tile is one call to <code>tile</code>. Read the plan before you type: every number in the calls is on it.</p><p>Tiles that touch share a number. The red tile is 400 wide and starts at 0, so the white tile beside it starts at <code>x = 400</code>. The top row is 300 tall, so every tile in the bottom row starts at <code>y = 300</code>. The probe prints the right edge of each tile in the top row, which should be 400 and 640.",
   "figure": plan_figure(),
   "prefix": SETUP + '\n' + TILE_DEF + '\n',
   "where": "Replace the two calls under the drawing comment with these six. The function stays where it is.",
   "next": {
     "q": "The red tile is <code>tile(RED, 0, 0, 400, 300)</code>. The white tile beside it fills the rest of the top row. What are its four numbers?",
     "hints": ["It starts where the red tile ends, at the top of the window.",
               "<code>x</code> is 0 plus 400. <code>y</code> is 0. It is as tall as the red tile. The window is 640 across, so its width is 640 take away 400.",
               {"text": "Fill the blanks.", "code": 'tile(WHITE, ____, 0, ____, 300)'}],
     "a": "<code>tile(WHITE, 400, 0, 240, 300)</code>. The other four calls follow the plan the same way: find where the tile starts, then how far it goes to the next line or the edge of the window.",
   },
   "code": MONDRIAN_CALLS + '\nprint(f"top row right edges: {0 + 400} and {400 + 240}")\nprint(f"bottom row bottom edges: {300 + 180} and {400 + 80}")',
   "run": "headless",
   "frames": 3,
   "predict": "Three tiles are white on a white canvas. Why can you still see them?",
   "reveal": "Because of the borders. The white fill is the same colour as the canvas, so it changes nothing you can see, but every tile also draws its black border, and that is what makes the white tiles look like tiles. The probe prints 400 and 640 for the top row and 480 and 480 for the bottom, which means every tile reaches the next tile or the edge of the window with no gap."},

  {"title": "Make it yours: one number per run",
   "teach": "Now change things. One number per run, and before each run say what will move. The three kinds of change: swap a colour name for another, move a tile by changing its <code>x</code> or <code>y</code>, or resize it by changing its <code>w</code> or <code>h</code>. A resize changes where the tile ends, so the tile next to it has to change too, or a gap opens.</p><p>Here the red tile has been made 300 wide instead of 400, and nothing else was changed.",
   "prefix": SETUP + '\n' + TILE_DEF + '\n',
   "where": "Change one number in the calls you already have. Run. Say what moved. Then change the next number.",
   "code": 'tile(RED, 0, 0, 300, 300)\ntile(WHITE, 400, 0, 240, 300)\ntile(BLUE, 0, 300, 160, 180)\ntile(WHITE, 160, 300, 240, 180)\ntile(YELLOW, 400, 300, 240, 100)\ntile(WHITE, 400, 400, 240, 80)\nprint(f"the red tile now ends at x = {0 + 300}, and the white one still starts at 400")',
   "run": "headless",
   "frames": 3,
   "predict": "The red tile now ends at 300 and the white tile beside it still starts at 400. What is between 300 and 400 in the top row?",
   "hint": ["Nothing was drawn there. What colour is the canvas underneath, and does it have a border?"],
   "reveal": "A white strip 100 wide with no black border on its left or right, so it does not look like a tile. It looks like a hole. To close it, the white tile has to start at 300 and be 340 wide, so that it ends at 640 again. Changing one tile's width changes where it ends, and its neighbour's <code>x</code> has to follow. That is the build."},
 ],
 "hinge": {"q": "From session 5: in <code>tile(RED, 40, 40, 200, 120)</code>, which word in the function is a parameter and which value in the call is an argument? What is <code>w</code> while this call runs, and what is it in the call right after, <code>tile(BLUE, 240, 40, 160, 120)</code>?",
           "a": "<code>color</code>, <code>x</code>, <code>y</code>, <code>w</code>, and <code>h</code> are the parameters: the blanks on the <code>def</code> line. <code>RED</code>, 40, 40, 200, and 120 are the arguments: the values in the call. The arguments fill the parameters in order, so <code>w</code> is 200 during the first call and 160 during the second. The function does not remember anything between calls; each call fills all five blanks again."},
 "brief": {
   "title": "Build: your own Mondrian",
   "intro": "You are making a picture of your own, and the plan comes first, on paper. Draw a rectangle for the window and write 640 along the top and 480 down the side. Cut it into tiles with straight lines: at least six tiles, and every line goes all the way to another line or to the edge. Then write the four numbers for each tile next to it. Tiles that touch share a number, so write the shared numbers once and copy them.",
   "minutes": 15,
   "steps": [
     "Plan it on paper: a 640 by 480 rectangle cut into at least six tiles. Write <code>x</code>, <code>y</code>, <code>w</code>, and <code>h</code> for every tile.",
     "Start from your chunk 5 file. Keep the setup, the function, and the loop exactly as they are, and delete the six calls.",
     "Write one call to <code>tile</code> per tile on your plan, one at a time. Run after each call and check that the tile landed where the plan says.",
     "Check the edges: for every pair of tiles that touch, the number where one ends is the number where the other starts. A gap with no border is a tile you have not drawn yet.",
     "Add a colour of your own. Pick three numbers from 0 to 255, give them a capitalised name next to the other colours, and use it in one call.",
   ],
   "expected_got": [
     ["Every tile on the plan appears in the window", ""],
     ["No gap: the whole window is covered by tiles with black borders", ""],
     ["Tiles that touch share a number in their calls", ""],
     ["A colour you named yourself appears in one tile", ""],
     ["The function tile is still three lines long", ""],
   ],
 },
 "exits": {
   "floor": "A window with one red tile and a black border, drawn by one call to <code>tile</code>, and you can say what each of the five arguments does.",
   "middle": "A Mondrian of your own: at least six tiles from your paper plan, covering the whole window, with a colour you named.",
   "stretch": "Let the computer pick the colours. Put <code>import random</code> at the top, make a list <code>colors = [RED, BLUE, YELLOW, WHITE]</code> under the colour lines, and use <code>random.choice(colors)</code> as the first argument in every call. Run it three times and say why no two runs match.",
 },
 "ledger": "Stamp 6: a colour is three numbers from 0 to 255, <code>(x, y, w, h)</code> is where a rectangle starts and how big it is, <code>y</code> grows down, the right edge is <code>x + w</code>, a fifth value makes a border instead of a fill, <code>def tile(color, x, y, w, h):</code> called once per tile. Write <code>x + w</code> on the card and say what it is.",
 "teacher": {
   "timing": [
     "0:00 retrieval opener, 10 min",
     "0:10 chunk 1, the window, typed and run, 10 min (the window opens behind VS Code; say so before anyone runs)",
     "0:20 chunks 2 and 3, one rectangle and its border, 15 min (project the figure; most of the room will want to change the numbers already, and that is fine)",
     "0:35 chunk 4, the tile function, 20 min (the core of the session; ask the room for every line before opening a hint)",
     "0:55 chunk 5, the six calls, 10 min (read the plan out loud first; the calls are copied)",
     "1:05 chunk 6, one number per run, 5 min",
     "1:10 build brief, 15 min (the paper plan takes most rooms five minutes; do not let anyone type before the plan has numbers on it)",
     "1:25 exits, ledger stamp, 5 min",
   ],
   "misconceptions": [
     ["Runs chunk 1 and says nothing happened.", "The window opened behind VS Code. Point at the taskbar. Say this before the first run, and it will still happen."],
     ["Puts <code>y = 300</code> to move a tile up.", "It moved down. <code>y</code> counts from the top. Have them put a finger on the top left corner of the window and slide it down 300 pixels. This comes back in session 11, so get it right now."],
     ["Gives <code>w</code> the number where the tile should end, so a tile that should end at 400 is 400 wide.", "<code>w</code> is how wide, not where it ends. Ask where the tile starts, then ask how far from there to where it should end. The probe print in chunk 2 is for exactly this; have them add one for their tile."],
     ["Leaves off the 10 and the whole tile turns black.", "A rectangle with no thickness is filled. Ask which line ran last and what it painted over. Ten seconds."],
     ["Puts the border line above the fill line.", "The fill paints over the border. Later drawing covers earlier drawing. Swap them."],
     ["Puts the <code>tile</code> calls under the loop, after <code>pygame.quit()</code>, and nothing appears.", "The loop only shows what was drawn before it started, and nothing after <code>pygame.quit()</code> runs with a window. Move the calls above the loop, under the comment."],
     ["Writes the arguments in the wrong order, <code>tile(40, 40, RED, 200, 120)</code>, and gets a TypeError.", "Read the error's last line, then read the <code>def</code> line. The arguments fill the parameters in order, so the colour has to be first. This is the hinge question; do not give the answer, ask the order."],
     ["Resizes one tile and does not see why there is a hole.", "Chunk 6. Ask where the tile ends now, and where its neighbour starts. The two numbers have to match."],
     ["Cannot close the window.", "Its own close button, not the terminal. If the loop has no <code>pygame.event.get()</code>, the window hangs; check the copied loop against chunk 1."],
   ],
   "standards": ["NY-5.G.1", "NY-6.EE.2", "MP7"],
   "routing": "If the room is slow, chunk 4 is the session: a working <code>tile</code> function and two calls is the floor, and chunk 5's six calls can be copied in the first ten minutes of session 7, which uses the same window code. If the room is fast, the build takes the whole fifteen minutes anyway, because the paper plan is the slow part. The stretch needs nothing from you: <code>random.choice</code> is session 3's and the list is session 3's. One student will ask for a circle or a diagonal line. Session 7 draws lines at any angle; say so and keep today to rectangles.",
 },
}
