# robofun-beginner-fall2026

Beyond Vibe Coding, beginner semester. Python for grades 5 to 8, Robofun Fall 2026,
110 West End Avenue. Two beginner sections, Monday and Friday, working through the
same thirteen required sessions. Session 6, the Mondrian, was added in October 2026,
so the last Monday session has no date yet and the Friday bonus session is no longer
scheduled; it stays on the site for anyone who wants it.

Homepage: https://silvermanjonathan.github.io/robofun-beginner-fall2026/beginner_semester_hub.html
(`beginner_semester_hub.html` at the repo root; there is no `index.html`)

## Pages

| File | What it is |
|---|---|
| `beginner_semester_hub.html` | Course home. Session list, both calendars, how a session runs. |
| `beginner_constraints.html` | The published code constraint list, dated 2026-09-12. One frame loop, one exclusion list. |
| `standards_map.html` | Every standard code used, with its full statement and CASE identifier. |
| `semester_ledger_card.html` | The printable one-page card. Thirteen stamp boxes, a reference strip, an error-name table. |
| `session01_printing_names_input.html` | Printing, names, and input |
| `session01_extra_cards.html` | Session 1 extra cards: silly story, age calculator, bug hunt. For a student who finishes the build early. |
| `session01_extra_cards_key.html` | The session 1 extra cards' answer key. Linked from the session 1 teacher panel only. |
| `session02_comparisons_and_gates.html` | Comparisons and gates |
| `session02_worksheet.html` | Session 2 worksheet: and, or, and the stopping condition (chunks 4 to 6). Printed, and typed into on the projector. |
| `session02_worksheet.pdf` | The same worksheet as a PDF for printing: four pages, US letter, one part per page. |
| `session02_worksheet_key.html` | The session 2 worksheet's answer key. Linked from the session 2 teacher panel only. |
| `session02_extra_cards.html` | Session 2 extra cards: three-question quiz, guess my number, bug hunt. |
| `session02_extra_cards_key.html` | The session 2 extra cards' answer key. Linked from the session 2 teacher panel only. |
| `session03_loops_counters_lists.html` | Loops, counters, and lists |
| `session03_extra_cards.html` | Session 3 extra cards: times table, coin flips, bug hunt. |
| `session03_extra_cards_key.html` | The session 3 extra cards' answer key. Linked from the session 3 teacher panel only. |
| `session04_rock_paper_scissors.html` | Rock paper scissors. Ends with an extension: rock paper scissors lizard Spock. |
| `session05_functions_that_return.html` | Functions that return a value |
| `session05_extra_cards.html` | Session 5 extra cards: letter grades, dice game, bug hunt. |
| `session05_extra_cards_key.html` | The session 5 extra cards' answer key. Linked from the session 5 teacher panel only. |
| `session06_mondrian_rectangles.html` | A Mondrian made of rectangles. The first pygame window: one `tile` function, written line by line, called once per tile. |
| `session07_angles_and_shapes.html` | Angles and shapes on screen |
| `session08_strings_as_data.html` | Strings as data |
| `session09_remainders_cipher_wheel.html` | Remainders and the cipher wheel |
| `session10_dictionaries.html` | Dictionaries |
| `session11_the_pygame_window.html` | The pygame window |
| `session12_grids_keys_game_state.html` | Grids, keys, and game state |
| `session13_commission_and_demo.html` | Commission and demo day |
| `friday_bonus_distance_and_bumpers.html` | Friday bonus: distance and bumpers |

## Environment

VS Code on the desktop, throughout. One graphics library, pygame, from session 6
onward: `pip install pygame`. There is no turtle in this course and no second
graphics library, because turtle does not run in our VS Code setup. Session 6 draws a
Mondrian out of rectangles and session 7 is a pygame drawing session carrying the
same angle arithmetic a turtle session would.

Students meet the frame loop twice, on purpose:

- **Sessions 6 and 7** hand it over as a working harness whose only job is to hold a
  finished drawing on screen. The drawing is done once onto a `pygame.Surface`
  above the loop, because the picture never changes.
- **Session 11** takes the same eight lines apart and moves the `fill` and the
  drawing inside the loop, because the picture now changes every frame. Its
  retrieval opener asks for those lines from memory.

Both placements are on the constraints page, in that order, so nobody has to guess
which one a given page uses.

If an earlier build was already uploaded, delete `session05_turtle_and_angles.html`,
`session04_functions_that_return.html`, `session04_extra_cards.html`,
`session04_extra_cards_key.html`, `session05_angles_and_shapes.html`,
`session06_strings_as_data.html`, `session07_debugging_clinic.html`,
`session06_angles_and_shapes.html`, `session07_strings_as_data.html`,
`session08_remainders_cipher_wheel.html`, `session09_dictionaries.html`,
`session10_the_pygame_window.html`, `session11_grids_keys_game_state.html`, and
`session12_commission_and_demo.html` from the live repo. None of them exist here
(the last seven were renumbered when the Mondrian session was added) and the hub no
longer links to them.

## Look and behaviour

**Palette: Lecture Light.** Built for a projector in a room with the lights on, which
is why it is a light theme. A projector adds light rather than removing it, so a dark
background becomes muddy grey on a wall under ambient light and low-contrast dark-on-dark
text disappears. Light ground, near-black text, three accents.

| Token | Hex | Used for |
|---|---|---|
| paper | `#F4F0E6` | page background, warm rather than glaring white |
| card | `#FFFDF7` | section panels |
| ink | `#17181B` | body text |
| ink-soft | `#4A4D53` | secondary text, kept dark enough to project |
| teal | `#0E4D52` | header band, headings, buttons, links |
| clay | `#9C2B22` | hinge question, teacher panel, stretch exit, warnings |
| ochre | `#8A5A00` / `#D99B12` | chunk labels, predict boxes, middle exit |
| green | `#1D5B39` | verified output boxes, opener, floor exit |

Every text and background pair clears WCAG AA for body text. The lowest ratio on any
page is 5.83 (ochre chunk labels on a card); most sit between 9 and 17. Base font is
18px with 15.5px code, sized to be read from the back of a room. No hairline borders:
rules are 2px and accent edges 6 to 8px, because 1px light-grey lines vanish when
projected. Nothing relies on colour alone; every coloured element also carries a text
label or a border-width cue.

**Code colors.** Every block of Python is colored the way VS Code's light theme colors
it, so the projected page and a student's editor look alike: control words purple
(`hk`), `def`, `True`, `and`, `or`, `in` and the `f` of an f-string blue (`hs`),
functions brown (`hf`), classes and modules teal (`hc`), variables navy (`hv`), CAPITAL
constants mid blue (`hn`), strings dark red (`hq`), escapes red (`he`), numbers dark
green (`hd`), comments green (`hm`); operators and brackets stay ink. The block is
`<pre class="py"><code>` on a white background with a visible border, and each color is
the VS Code hue darkened until it clears 7:1 contrast on white; `render.py` computes
the ratios and stops the build if one falls short. The same colors print. Color only,
never bold or italic, so every character keeps its width. Output boxes, the
expected/got sheets, and code inside a sentence stay plain. `build/hl.py` (copied from
the Advanced Python course, with its module list trimmed to pygame, random, math, and
time) adds the color when the page is built and asserts that stripping its spans gives
back the snippet exactly.

**Code size.** Code blocks and output boxes are 19px, a little over the 18px prose, so
they read from the back of the room. The page column is 1080px wide to fit them, and
paragraphs and list items are capped at 72ch so prose lines stay at reading length. On
a phone (760px and under) code is 15px and a wide table scrolls inside itself, so the
page never scrolls sideways. In print the code keeps its old 15.5px, so printed pages
and the PDFs do not reflow.

**Hints nest.** Every hint on the site opens one inside the next, the way the
Advanced course's ladders do: hint 2's button sits inside hint 1's box, and the
button that shows the answer, the line, or the real output sits inside the last
hint. So the hints come out in order and nothing can be opened out of turn. This
holds for the per-line "What goes next?" ladders, the hints on predict questions, and
the clues on the extra cards' bug hunts. `render.nest_hints` is the one function
that builds them. The session 5 build brief writes its three tools (`total_of`,
`tallest_of`, `average_of`) line by line this way, and session 6 writes `tile` the
same way.

**Indent guides in the hints.** Inside every hint ladder (the per-line "What goes
next?" ladders, the hints on predict questions, and the extra cards' clues), code
shows the indent guides VS Code draws: a bar down each four-space step of
indentation, so a single line shown on its own still shows how far in it goes. They
are 6px wide in `#595959` (7:1 on white, checked in `render.py` with the code
colors), not VS Code's 1px light grey, because thin light lines wash out on the
projector. The bars run unbroken through blank lines inside a block, as they do in
VS Code. `render.indent_guides` puts each step's four spaces in a
`<span class="ig">` in every code block on the site, but only blocks inside the
hints draw them; the rule is one CSS selector, so other blocks can have them later
by widening it. The spaces stay spaces, so copied code keeps its indentation. The
bars are borders, so they print.

**Reveals hide the real output.** Each chunk shows the code, then the prediction
question, then a button reading "Run it first, then check here". The button reveals
the verified terminal output *and* the explanation together. Nothing about what the
program prints is visible until the button is clicked, so a projected page cannot
give the answer away before students commit to a prediction. `validate.py` does not
check this; a separate check confirms no `<pre class="out">` block renders outside a
hidden `.ans` container.

## Repo conventions

- Flat repo. No subdirectories, no `index.html`. The hub is the homepage.
- All CSS and JavaScript inline in each file. Google Fonts is the only external
  dependency.
- No `localStorage`, no `sessionStorage`, no `indexedDB`. These pages are embedded
  in Google Sites by full-page URL and storage is blocked inside the iframe.
- Internal links carry a version pin: `?v=14`. Bump the pin on every page whose
  content changes, so the embed does not serve a cached copy.
- Re-upload the hub whenever a page is added, renamed, or removed, or the
  navigation will have gaps.
- Zero em-dash and en-dash characters anywhere in the prose. The validator fails
  the build if one appears.

## Standards

Every code on the site was resolved through the Learning Commons Knowledge Graph
connector on 2026-09-12 and printed with its CASE identifier so it can be checked.
Nothing was written from memory.

- New York Next Generation Mathematics: NY-4.MD.5, NY-4.OA.3, NY-5.OA.2, NY-5.OA.3,
  NY-5.G.1, NY-5.G.2, NY-6.EE.2, NY-6.EE.5, NY-6.EE.9, NY-6.NS.6, NY-6.NS.8,
  NY-6.SP.4, NY-8.F.1, NY-8.G.7
- Standards for Mathematical Practice, Multi-State: MP1, MP6, MP7, MP8
- New York Next Generation ELA: 5R3, 5W2, 5SL4

At most three per session, footered as "mapped to" rather than "aligned with".

No computer science standard appears anywhere on this site. The connector returned
nothing for the New York Computer Science and Digital Fluency codes or for CSTA
codes. When those codes are in hand, add at most three per session and keep the
"mapped to" wording.

## Build

The HTML is generated. Edit the content files, not the HTML.

```
build/standards.py     the resolved standards registry
build/sessions_a.py    sessions 1 to 4
build/session06.py     session 6, the Mondrian (added October 2026)
build/sessions_b.py    sessions 5, 7, 8, and 9
build/sessions_c.py    sessions 10 to 13 and the Friday bonus
build/render.py        runs every snippet, then writes the site
build/validate.py      checks the written site
build/hl.py            colors Python code the way VS Code does; copied from the Advanced course
build/worksheet.py     the worksheet CSS, blocks, and projector typing script, shared by every sheet
build/ws02.py          the session 2 worksheet and its answer key
build/extras.py        the extra cards and their answer keys, sessions 1 to 3 and 5
build/graphs.py        session 4's figures: the rules as arrows, and the tree of pairs
build/pdf.py           renders the worksheets to PDF
```

```
pip install pygame --break-system-packages
python3 build/render.py
python3 build/pdf.py
python3 build/validate.py
```

`pdf.py` needs WeasyPrint (`brew install weasyprint` on a Mac). Run it after
`render.py` whenever a worksheet changes, then check the PDF's fonts are DM Sans,
JetBrains Mono, and Bricolage Grotesque; a machine that cannot reach Google Fonts and
does not have them installed falls back to its own fonts.

## Verification

`render.py` executes every code snippet and pastes the real captured output into
the page. No output box on this site was typed from expectation.

- Terminal snippets run under CPython 3.12, with real keystrokes piped in where the
  program calls `input`.
- pygame snippets run headless with `SDL_VIDEODRIVER=dummy` and
  `SDL_AUDIODRIVER=dummy`. `pygame.event.get` is patched to inject a QUIT event
  after a set number of frames, and `pygame.key.get_pressed` is patched to simulate
  held keys, so the printed probe lines on those pages are real.
- Every snippet was executed. Nothing is syntax checked only. Where a chunk
  continues a program from an earlier chunk, the page says so on the page itself and
  the whole file was run together, with the earlier program supplied as a run prefix.
- Snippet files are named after their session, so tracebacks shown to students read
  `File "Jonathan_session02.py", line 3` rather than a temporary path. The house
  rule is that every student file starts with the student's first name, then an
  underscore, then the session; Jonathan stands in for the name on the pages.
- Output labels only claim a frame quota when the snippet actually contains a loop.
- A chunk or card with a `seed` runs with `random` seeded before the program starts,
  through the same `sitecustomize` hook, so a program that picks at random prints the
  same run every build and keeps its line numbers. The page labels that box "on one
  run" and the prose says the student's run will differ.

`validate.py` checks tag balance, reveal-button to answer-block parity, duplicate
reveal ids, `aria-controls` and `aria-expanded` on every reveal button, escaped angle
brackets inside `<pre>` blocks (with the color spans stripped first), that every
`<pre><code>` block carries the `py` class and only `hl.py`'s color classes and the
indent guide class, that every step of indentation in a code block sits in a guide
span, that no
output box carries color spans, absence of storage APIs, dash characters, banned
filler phrases (including any mention of a summer camp or another course), dead
internal links, the presence of a title and an h1 on every page, that every teacher
panel's timing rows sum to 90 minutes and include a ledger stamp row, and that no
captured `input()` prompt appears without the typed answer after it.

Terminal snippets that call `input()` run with a `sitecustomize` hook that echoes
the piped answer after the prompt, so the output box reads the way a student's
terminal does. The hook is installed on `builtins`, not prepended to the source, so
traceback line numbers are unchanged.

Chunks may carry a `hint` (a string or a list): each hint renders as its own
"Show a hint" button inside the predict box, above the run-it-first button, and
counts toward reveal parity.

A session with a `worksheet` entry gets a toolbar under its masthead (open the
worksheet, download the PDF) and a Files note in its teacher panel with the key.
`render.py` writes the sheet and key from `build/wsNN.py`. The sheet's programs are
read from the session's own chunks, so they cannot differ from the page. Every True or
False on the sheet and key is Python's own comparison, and every printed line in the
key comes from running the program at build time; the build stops if a run disagrees
with a row or with a number in a sentence.

Build briefs may carry `cards`: verified code blocks inside the brief (session 12's
engine). They run through the same harness as chunks and their output sits behind
the same reveal.

A session with an `extension` entry gets a section after "Where you can stop" for a
student who is past the stretch exit: an intro, verified `cards` with the same
reveal, numbered steps, and an expected and got table. Session 4 uses it for rock
paper scissors lizard Spock.

A chunk with a `steps` entry is taught one line at a time. The program so far (the
previous chunk's code, or the chunk's own `start`) sits behind a button; then each
step is a question for the room, "Line 9. What goes next?", with hints that open one
inside the next (hint 2's button is inside hint 1's box), the last hint being the line
with one blank written as `____`, and a final button that shows the line; then the
whole program sits behind a button. Each step's `label` names its line number, and
`render.py` checks the label and the line against the chunk's program, so a number
cannot drift from the code. A chunk or extension card with a `next` entry instead asks
one question for the whole block. Session 4 uses `steps` on chunks 2 to 8 and `next`
on the extension.

A session with an `extras` entry gets a section under "Where you can stop" that links
to its extra cards, and a Files note in its teacher panel with the answer key.
`render.py` writes both pages from `build/extras.py`. The cards are for a student who
finishes the build while the teacher is working with someone else: three programs per
session, two to write or finish and one short broken program to fix. A card uses only
what the course has taught by the end of its session. Every program on a card, every
stage of every bug hunt, and each Go further version is run at build time; the
finished runs, the error messages in the key, and the numbers the sentences quote come
from those runs, and the build stops if a run disagrees with a sentence, a clue, or a
table. A finished run on a card is shown openly, because it is the thing to aim for;
it uses the class `want`, not `out`, so the rule that no `out` block shows outside a
reveal still holds. Clues sit behind one button each. The card pages print from the
browser, one card to a sheet, with the clues printed and the answers left off.

## Known gaps

- Float topics are listed on the hub but not built: file input and output for a high
  score that survives a restart, sine waves and circular motion, coaster energy
  stages. A GUI float was removed: tkinter is not available, and a pygame version
  would need on-screen labels, which `pygame.font` is excluded from providing.
- The calendar assumes closures on Mon Sep 21, Mon Oct 12, and Fri Nov 27. Fri Oct 2
  falls in the intermediate days of Sukkot. Check the published Robofun closure list
  before committing a syllabus to families.
- Session 11 is the fullest session of the term and will not finish in 90 minutes.
  Nothing carries over between sessions; session 12 hands out a finished version
  of the session 11 room as its engine, printed on the page and verified at build
  time. The teacher copies it onto every machine, named in the house style
  (`Ada_session12.py`), before class.

## Printing history

- **2026-09-12, v5.** First build.
- **2026-09-13, v6.** Review round. Faults found and fixed, all of the kind neither
  guard could see: session 12 described an engine that existed nowhere; session 7's
  build referred to five broken cards that were not on the page; session 4 presented
  `def` as revision from a summer camp these students did not attend, and eleven
  passages across six pages referred to that camp; session 2's hinge described a text
  comparison that Python 3 does not perform (it raises TypeError); four pages said
  `python -c "import pygame"` prints nothing (pygame 2 prints a two-line greeting);
  sessions 6, 9, 11 and 12 planned for build work to carry over across a cold start;
  ten teacher panels gave the ledger stamp no time; session 3 miscounted how often
  `tallest` changes; `input()` output boxes showed prompts with no typed answer.
  Open decisions resolved: the tkinter float is dropped (no labels without
  `pygame.font`); if Fri Oct 2 is lost, the bonus date absorbs it. New checks added
  to `validate.py` for the classes of fault that could be mechanised.
- **2026-09-29, v7.** Session 2 worksheet added: and, or, and the while loop's stopping
  condition (chunks 4 to 6). Sheet, answer key, and a four-page PDF with one part per page, each program on
  the same page as its table. The worksheet helpers from the Advanced course
  now live in `build/worksheet.py` for every beginner sheet. The session 2 page gets a
  worksheet toolbar and a Files note in its teacher panel. `validate.py` accepts links
  to any file in the site (the PDF). Code blocks on every page are now coloured by
  role, VS Code Light+ style (`build/highlight.py`). Version pin bumped to `?v=7` on
  every page. `build/standards.py` added: the original was never committed, so it was
  rebuilt from the published standards map and session pages; the build reproduces
  every page byte for byte from it.
- **2026-10-05, v8.** Extra cards added for sessions 1 to 4 (`build/extras.py`): a card
  page and an answer key per session, twelve cards in all. Each session page links its
  cards under "Where you can stop", and each teacher panel links the key. Sessions 5
  onward have none yet. Version pin bumped to `?v=8` on every page. Built with Python
  3.11, which reproduces the v7 pages byte for byte; under 3.12 and 3.13 the same
  sources give the same colours but split f-string quote marks into their own spans,
  and one traceback on the session 7 page draws its caret line differently.
- **2026-10-18, v9.** A new session 4, rock paper scissors, inserted after session 3:
  eight chunks that build the game from the move list, a five-way gate, rounds,
  counters, the verdict, and the asking loop, with a first-to-three build and an
  extension for rock paper scissors lizard Spock. The debugging clinic is dropped.
  Functions that return becomes session 5, angles and shapes session 6, strings as
  data session 7, each on the next date; sessions 8 to 12 and the bonus keep their
  dates. Every cross-reference, stamp number, and the constraints page's "first
  taught" column renumbered. Session 8's opener retrieves the remainder from session
  6 in place of the clinic's bug types; session 12's card questions point at the
  reference strip's one-change-per-run line. Session 3's rock paper scissors extra
  card is replaced by coin flips, so the card does not give session 4 away, and the
  functions cards move to session 5 with `session05_` file names. `render.py` gains
  `seed` on chunks and cards, an `extension` section, and a fix for the hook's
  bytecode cache, which could hand one seeded run the previous run's seed. Version
  pin bumped to `?v=9` on every page.
- **2026-10-18, v10.** Session 4 reworked for the room. Chunks 2 to 8 and the
  extension card now open with a "What goes next?" question whose hints open one
  inside the next, the third being the code with one blank, and whose last button is
  the only place the chunk's code appears (`next` on a chunk, `ladder` in
  `render.py`). Three figures from `build/graphs.py`: the rules as arrows for three
  moves (chunk 4) and for five (the extension), and the tree of the six pairs that
  are not ties (chunk 3). A scoreboard line prints after every round from chunk 6
  on, and the build puts the ties counter on it. Version pin bumped to `?v=10`.
- **2026-10-18, v11.** Two style changes, no content changes. Python code is colored
  at build time the way VS Code does, by `build/hl.py` from the Advanced course (ten
  token classes, each color darkened to at least 7:1 on a white code background,
  checked in `render.py`); every code block is now `<pre class="py"><code>`, output
  and sheets stay plain, and the ledger card's reference strip colors only its code
  column. Code and output go from 15.5px to 19px, the column from 900px to 1080px
  with prose capped at 72ch, 15px code on phones with tables that scroll inside
  themselves, and the old 15.5px kept in print. Checked in Chromium at 1280px with
  every reveal open: the same 4 of 264 code blocks scroll sideways before and after
  (the longest `while` line in sessions 4, 5's key, 6, and 12), none new; at 390px no
  page scrolls sideways. Every page's prose and every block's plain text are byte for
  byte what they were. `session02_worksheet.pdf` re-rendered: same four pages, same
  five embedded fonts, white code boxes with the new colors. Version pin `?v=11`.
- **2026-10-18, v12.** Session 4 taught one line at a time: chunks 2 to 8 each open
  with the program so far behind a button, then one "What goes next?" question per
  new line, with hints that open one inside the next and the line behind the last
  button (`steps` on a chunk; the labels are checked against the code at build time).
  The game is finished at chunk 6; keeping score and the match verdict follow as two
  modifications to the working program, each line by line. The five-move figure's
  verbs now sit on their own arrows, in boxes the arrow passes through, placed by a
  clearance search so none lands on a crossing. Prose pass over the session for plain
  wording. Version pin `?v=12`.
- **2026-10-26, v14.** Indent guides in the hints, the way VS Code shows them but
  6px wide and dark grey so they survive the projector (see "Indent guides in the
  hints" above). No content changes: with the guide spans removed, every page is
  byte for byte what it was apart from the CSS and the pin. Checked in Chromium at
  1280px and 390px with every reveal open: every page is the same height as before,
  and the same code blocks scroll sideways, none new. The worksheet has no hints, so
  `session02_worksheet.pdf` was not re-rendered. Version pin `?v=14`.
