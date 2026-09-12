# robofun-beginner-fall2026

Beyond Vibe Coding, beginner semester. Python for grades 5 to 8, Robofun Fall 2026,
110 West End Avenue. Two beginner sections, Monday and Friday, working through the
same twelve required sessions. Friday has one extra date and spends it on a bonus
session that nothing later depends on.

Homepage: `beginner_semester_hub.html`

## Pages

| File | What it is |
|---|---|
| `beginner_semester_hub.html` | Course home. Session list, both calendars, how a session runs. |
| `beginner_constraints.html` | The published code constraint list, dated 2026-09-12. One frame loop, one exclusion list. |
| `standards_map.html` | Every standard code used, with its full statement and CASE identifier. |
| `semester_ledger_card.html` | The printable one-page card. Twelve stamp boxes, a reference strip, an error-name table. |
| `session01_printing_names_input.html` | Printing, names, and input |
| `session02_comparisons_and_gates.html` | Comparisons and gates |
| `session03_loops_counters_lists.html` | Loops, counters, and lists |
| `session04_functions_that_return.html` | Functions that return a value |
| `session05_angles_and_shapes.html` | Angles and shapes on screen |
| `session06_strings_as_data.html` | Strings as data |
| `session07_debugging_clinic.html` | Debugging clinic |
| `session08_remainders_cipher_wheel.html` | Remainders and the cipher wheel |
| `session09_dictionaries.html` | Dictionaries |
| `session10_the_pygame_window.html` | The pygame window |
| `session11_grids_keys_game_state.html` | Grids, keys, and game state |
| `session12_commission_and_demo.html` | Commission and demo day |
| `friday_bonus_distance_and_bumpers.html` | Friday bonus: distance and bumpers |

## Environment

VS Code on the desktop, throughout. One graphics library, pygame, from session 5
onward: `pip install pygame`. There is no turtle in this course and no second
graphics library, because turtle does not run in our VS Code setup. Session 5 is a
pygame drawing session carrying the same angle arithmetic a turtle session would.

Students meet the frame loop twice, on purpose:

- **Session 5** hands it over as a working harness whose only job is to hold a
  finished drawing on screen. The drawing is done once onto a `pygame.Surface`
  above the loop, because the picture never changes.
- **Session 10** takes the same eight lines apart and moves the `fill` and the
  drawing inside the loop, because the picture now changes every frame. Its
  retrieval opener asks for those lines from memory.

Both placements are on the constraints page, in that order, so nobody has to guess
which one a given page uses.

If an earlier build was already uploaded, delete `session05_turtle_and_angles.html`
from the live repo. It no longer exists here and the hub no longer links to it.

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
- Internal links carry a version pin: `?v=3`. Bump the pin on every page whose
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
build/sessions_b.py    sessions 5 to 8
build/sessions_c.py    sessions 9 to 12 and the Friday bonus
build/render.py        runs every snippet, then writes the site
build/validate.py      checks the written site
```

```
pip install pygame --break-system-packages
python3 build/render.py
python3 build/validate.py
```

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
  `File "session07.py", line 3` rather than a temporary path.
- Output labels only claim a frame quota when the snippet actually contains a loop.

`validate.py` checks tag balance, reveal-button to answer-block parity, duplicate
reveal ids, escaped angle brackets inside `<pre>` blocks, absence of storage APIs,
dash characters, banned filler phrases, dead internal links, and the presence of a
title and an h1 on every page.

## Known gaps

- Float topics are listed on the hub but not built: file input and output for a high
  score that survives a restart, sine waves and circular motion, coaster energy
  stages, and one GUI session. The GUI float previously assumed tkinter and needs
  rethinking, since tkinter is not available.
- The calendar assumes closures on Mon Sep 21, Mon Oct 12, and Fri Nov 27. Fri Oct 2
  falls in the intermediate days of Sukkot. Check the published Robofun closure list
  before committing a syllabus to families.
- Session 11 is the fullest session of the term and will not finish in 90 minutes.
  Its build brief is planned to continue into session 12.
