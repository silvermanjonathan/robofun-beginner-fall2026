"""Extra cards for sessions 1 to 3 and 5: three more programs per session for a student who
finishes the build with time left.

Each session gets a card page for the student and an answer key for the teacher. Card A
and card B are programs to write or finish; card C is a short broken program to fix.
A card uses only what the course has taught by the end of its session, and nothing a
later session teaches.

Every program on a card is run with render.run_snippet when the site is built. The
finished runs, the error messages in the key, and every number a sentence quotes come
from those runs. The build stops if a run disagrees with a sentence, a clue, or a table.

A session opts in with an "extras" entry in its sessions_*.py dict:
    "extras": {"slug": "session01_extra_cards", "cards": [three card titles]}
render.py then writes the two pages, links the cards from the session page under
"Where you can stop", and links the key from the teacher panel only.
"""

import html
import re

import render

EXTRA_CSS = """
<style>
pre.want{background:var(--green-tint); border-color:#A9C6B2; border-left:6px solid var(--green);
  color:var(--green-ink)}
.tscroll{overflow-x:auto; margin:0 0 16px}
.tscroll table{margin:0}
section.xcard h3{margin-top:20px}
.xkey td code{white-space:normal}
@media (max-width:760px){
  main{padding:22px 16px 8px} header.top{padding:24px 16px 20px} section{padding:18px 16px}
  .tscroll table{min-width:560px} th,td{padding:7px 8px}
}
@media print{
  @page{size:letter; margin:12mm 14mm 14mm}
  body{font-size:11pt; line-height:1.4} main{padding:0}
  header.top{padding:4px 0 4px; margin-bottom:8px}
  header.top .dates,header.top .sub{display:none} header.top h1{font-size:18pt; margin:0 0 4px}
  nav.pager,footer,.toolbar{display:none}
  section{padding:10px 14px; margin:0 0 10px; border-width:1.5px}
  p{margin:0 0 7px} li{margin:0 0 4px} ul,ol{margin:0 0 8px}
  h2{font-size:16pt; margin:0 0 6px} h3,section.xcard h3{font-size:12.5pt; margin:8px 0 4px}
  .chunk-no,.outlabel{font-size:9pt; margin:0 0 4px}
  /* one card per printed sheet: the first card shares a page with the short list above it,
     and each later card starts a new page; a long card may run on to a second page */
  section.xcard{break-inside:auto}
  section.xcard ~ section.xcard{break-before:page}
  pre,tr,p,li{break-inside:avoid} h2,h3,.chunk-no,.outlabel{break-after:avoid}
  pre{white-space:pre-wrap; overflow-wrap:anywhere; font-size:9.5pt; line-height:1.4;
    padding:8px 12px; margin:0 0 8px}
  table{font-size:10.5pt; margin:0 0 8px} th,td{padding:4px 8px}
  /* on paper there is nothing to click: clues print, answers do not */
  button.rev{display:none} .hints .ans{display:block; border-top:0; padding-top:0; margin:0 0 4px}
  .predict{border:1.5px dashed #666; background:#fff; padding:8px 12px; margin:0 0 8px}
  .predict p{margin:0}
}
</style>
"""
HEAD = EXTRA_CSS

KEY = {"on": False}
SESS = {s["num"]: s for s in render.SESSIONS}


# ------------------------------------------------------------------ running

def fname(n, tail):
    """The file name a card asks for, in the house style."""
    return "Jonathan_session%02d_%s.py" % (n, tail)


def run(src, typed=None, seed=None, name="Jonathan_extra.py", tag="extra"):
    """Run a card program the way the session pages run theirs; return (output, exit code).

    typed is the list of answers typed at the input prompts. seed fixes random.choice,
    so a card can show one real run of a program that is different every time.
    """
    stdin = None if typed is None else "".join(t + "\n" for t in typed)
    pre = "" if seed is None else "import random\nrandom.seed(%d)\n" % seed
    out, rc = render.run_snippet(src, stdin=stdin, preamble=pre, fname=name)
    assert out != "TIMEOUT", tag
    render.VERIFY_LOG.append([tag, "py", "rc=" + str(rc), str(len(out.splitlines())) + " lines"])
    return out, rc


def ok(src, typed=None, seed=None, name="Jonathan_extra.py", tag="extra"):
    """Run a program that must finish without an error; return its output."""
    out, rc = run(src, typed, seed, name, tag)
    assert rc == 0, tag + " should run cleanly:\n" + out
    return out


def edit(src, old, new):
    """Return src with one exact piece replaced; the piece must appear exactly once."""
    assert src.count(old) == 1, "expected exactly one of: " + old
    return src.replace(old, new)


def error_line(out):
    """Return the line number the last traceback entry names."""
    hits = re.findall(r'line (\d+)', out)
    assert hits, out
    return int(hits[-1])


# ----------------------------------------------------------------- blocks

def esc(s):
    return html.escape(s, quote=False)


def c(s):
    """Inline code."""
    return "<code>" + esc(s) + "</code>"


def want(text, label="A finished run"):
    """A real run shown on the card as the thing to aim for."""
    return ('<p class="outlabel">' + label + '</p><pre class="want">'
            + html.escape(text) + '</pre>')


def steps(items):
    return "<ol>" + "".join("<li>" + x + "</li>" for x in items) + "</ol>"


def file_line(n, tail):
    return ("<p>Make a new file called " + c(fname(n, tail))
            + ", with your own first name in place of Jonathan.</p>")


def ask(idx, label, question, answer):
    """A question with its answer behind a button; in the key, the answer is shown."""
    if KEY["on"]:
        return ('<p><b>' + label + ':</b> ' + question + '</p><p class="note">' + answer + '</p>')
    return render.reveal(idx, question, answer, label, "", "Show the answer", "Hide the answer")


def clues(idx, items):
    """The clues, one inside the next, so clue 2 opens only after clue 1; the key leaves them out."""
    if KEY["on"]:
        return ""
    return ('<p><b>Clues, if you are stuck.</b> Open one at a time. The next clue is inside '
            'the one before it.</p>' + render.nest_hints(idx, items, "", prefix="-clue", word="Clue"))


def table(headers, rows, cls=""):
    out = '<div class="tscroll"><table' + (' class="' + cls + '"' if cls else "") + "><tr>"
    out += "".join("<th>" + h + "</th>" for h in headers) + "</tr>"
    for r in rows:
        out += "<tr>" + "".join("<td>" + x + "</td>" for x in r) + "</tr>"
    return out + "</table></div>"


def card(letter, kind, minutes, title, body, bug=False):
    cls = "hinge xcard" if bug else "chunk xcard"
    return ('<section class="' + cls + '"><p class="chunk-no">Card ' + letter + ' &middot; ' + kind
            + ' &middot; about ' + str(minutes) + ' minutes</p><h2>' + esc(title) + '</h2>'
            + body + '</section>')


BUG_RULES = steps([
    "Run it.",
    "If there is an error, read its last line first.",
    "Fix one thing. Run it again.",
    "Keep going until the output matches the finished run above.",
]) + "<p>For each bug, write down the line number and what you changed.</p>"


def bug_table(n, tail, stages, typed, tag):
    """Run every stage of a bug hunt and return the key's table rows.

    A stage is the program as it stands before one fix. kind "error" must stop with the
    named error on the named line; kind "wrong" and "done" must run cleanly and print
    the lines listed in "shows".
    """
    rows = []
    for k, st in enumerate(stages):
        out, rc = run(st["code"], st.get("typed", typed), name=fname(n, tail),
                      tag="%s-run%d" % (tag, k + 1))
        printed = out.splitlines()
        for ln in st.get("shows", []):
            assert ln in printed, (tag, k + 1, ln, out)
        shown = ", ".join(c(ln) for ln in st.get("shows", []))
        if st["kind"] == "error":
            assert rc != 0 and st["expect"] in printed[-1], (tag, k + 1, out)
            assert error_line(out) == st["line"], (tag, k + 1, out)
            sees = (shown + ", then " if shown else "") + c(printed[-1]) + ", on line " + str(st["line"])
        else:
            assert rc == 0, (tag, k + 1, out)
            sees = st.get("sees", shown)
        rows.append([str(k + 1), sees, st.get("bug", "None left"), st.get("fix", "")])
    return rows


def bug_key(rows, final, note=""):
    b = table(["Run", "What the student sees", "The bug", "The fix"], rows, "xkey")
    if note:
        b += "<p>" + note + "</p>"
    return b + "<p>The fixed program:</p>" + render.code_block(final)


# =================================================================== session 1

STORY = '''animal = input("Name an animal: ")
food = input("Name a food: ")
place = input("Name a place: ")
number = input("Pick a whole number: ")
number = int(number)
double = number * 2

print(f"One day the {animal} walked into {place}.")
print(f"It ordered {number} plates of {food}.")
print(f"Then it changed its mind and ordered {double}.")
'''
STORY_TYPED = ["penguin", "tacos", "the library", "7"]

AGE = '''name = input("Your name: ")
age = input("Your age in years: ")
age = int(age)

days = age * 365
hours = days * 24
later = age + 10

print(f"{name}, you are about {days} days old.")
print(f"That is about {hours} hours.")
print(f"In 10 years you will be {later}.")
'''
AGE_TYPED = ["Ada", "11"]
AGE_MORE = edit(edit(AGE, "later = age + 10\n",
                     "minutes = hours * 60\nseconds = minutes * 60\nlater = age + 10\n"),
                'print(f"In 10 years',
                'print(f"That is about {minutes} minutes.")\n'
                'print(f"That is about {seconds} seconds.")\nprint(f"In 10 years')

SNACK = '''snack = input("Which snack? ")
count = input("How many bags? ")
extra = count + 1
print("You get {extra} bags of {snak}. One is free.")
'''
SNACK_TYPED = ["pretzels", "3"]


def session1():
    n = 1
    # ---- card A
    story_out = ok(STORY, STORY_TYPED, name=fname(n, "story"), tag="x1a")
    no_int = edit(STORY, "number = int(number)\n", "")
    no_int_last = ok(no_int, STORY_TYPED, name=fname(n, "story"), tag="x1a-noint").splitlines()[-1]
    assert story_out.splitlines()[-1].endswith("ordered 14.") and no_int_last.endswith("ordered 77.")
    a = ("<p>You make a program that asks four questions, then prints a three-line story that "
         "uses the answers.</p>" + file_line(n, "story") + want(story_out)
         + steps([
             "Ask the four questions with <code>input</code>. Store each answer in its own variable.",
             "The number comes back as text. Change its type with <code>int()</code>, on a line of its own.",
             "Make a new variable called <code>double</code>. Its value is the number times 2. "
             "The times sign in Python is <code>*</code>.",
             "Print the three story lines. Each one is an f-string.",
         ])
         + ask("x1a-try", "Try it",
               "Take out the <code>int()</code> line and run the program again with 7. What does "
               "the last line print now? Put the line back afterwards.",
               c(no_int_last) + " Without <code>int()</code>, <code>number</code> is the text 7. "
               "Text times 2 is the same text written twice.")
         + "<h3>Go further</h3><p>Add a fifth question and a fourth story line that uses its "
           "answer. Then change the story to one of your own.</p>")
    if KEY["on"]:
        a = render.code_block(STORY) + want(story_out, "What it prints") + ask(
            "x1a-try", "Try it", "the program without its <code>int()</code> line, run with 7.",
            "The last line is " + c(no_int_last) + " Text times 2 is the same text written twice.")

    # ---- card B
    age_out = ok(AGE, AGE_TYPED, name=fname(n, "age"), tag="x1b")
    swapped = edit(AGE, "days = age * 365\nhours = days * 24\n", "hours = days * 24\ndays = age * 365\n")
    sw_out, sw_rc = run(swapped, AGE_TYPED, name=fname(n, "age"), tag="x1b-swapped")
    sw_last = sw_out.splitlines()[-1]
    assert sw_rc != 0 and sw_last.startswith("NameError: name 'days' is not defined"), sw_out
    more_out = ok(AGE_MORE, AGE_TYPED, name=fname(n, "age"), tag="x1b-more")
    minutes = re.search(r"That is about (\d+) minutes\.", more_out).group(1)
    seconds = re.search(r"That is about (\d+) seconds\.", more_out).group(1)
    assert int(minutes) == 11 * 365 * 24 * 60 and int(seconds) == int(minutes) * 60
    b = ("<p>You make a program that asks for a name and an age, then prints how old that "
         "person is in days and in hours.</p>" + file_line(n, "age") + want(age_out)
         + steps([
             "Ask for the name and the age. Change the type of the age to a number.",
             "Make a variable called <code>days</code>. Its value is the age times 365.",
             "Make a variable called <code>hours</code>. Its value is <code>days</code> times 24.",
             "Make a variable called <code>later</code>. Its value is the age plus 10.",
             "Print the three sentences. Each one is an f-string.",
         ])
         + ask("x1b-before", "Before you run",
               "Suppose the line that makes <code>hours</code> came before the line that makes "
               "<code>days</code>. What would Python do?",
               "It stops with " + c(sw_last) + " Python runs the lines from the top. On the "
               "<code>hours</code> line, <code>days</code> has no value yet.")
         + "<p><b>Check:</b> run it with Ada and 11. Your three lines should match the finished "
           "run above.</p>"
           "<h3>Go further</h3><p>Add minutes and seconds, each with its own printed sentence. "
           "An hour has 60 minutes and a minute has 60 seconds. For age 11 the program should "
           "print " + minutes + " minutes and " + seconds + " seconds.</p>")
    if KEY["on"]:
        b = (render.code_block(AGE) + want(age_out, "What it prints")
             + "<p><b>Before you run:</b> with the two lines the other way round it stops with "
             + c(sw_last) + "</p><p><b>Go further:</b> <code>minutes = hours * 60</code> and "
             "<code>seconds = minutes * 60</code>, each with its own print line. For age 11 they "
             "print " + minutes + " and " + seconds + ".</p>")

    # ---- card C
    s2 = edit(SNACK, 'count = input("How many bags? ")\n',
              'count = input("How many bags? ")\ncount = int(count)\n')
    s3 = edit(s2, 'print("You get', 'print(f"You get')
    s4 = edit(s3, "{snak}", "{snack}")
    final_out = ok(s4, SNACK_TYPED, name=fname(n, "bugs"), tag="x1c-final")
    last = final_out.splitlines()[-1]
    rows = bug_table(n, "bugs", [
        {"code": SNACK, "kind": "error", "expect": "TypeError", "line": 3,
         "bug": "<code>count</code> is still text", "fix": "Add <code>count = int(count)</code> under line 2"},
        {"code": s2, "kind": "wrong", "shows": ["You get {extra} bags of {snak}. One is free."],
         "bug": "The string has no <code>f</code>, so the braces print",
         "fix": "Put <code>f</code> in front of the opening quote mark"},
        {"code": s3, "kind": "error", "expect": "NameError: name 'snak' is not defined", "line": 5,
         "bug": "<code>snak</code> is misspelled", "fix": "Change <code>snak</code> to <code>snack</code>"},
        {"code": s4, "kind": "done", "shows": [last]},
    ], SNACK_TYPED, "x1c")
    cc = ("<p>This program has 3 bugs. When you type pretzels and 3, it is supposed to print "
          "this:</p>" + want(final_out)
          + file_line(n, "bugs") + "<p>Type the program exactly as it is here, bugs and all:</p>"
          + render.code_block(SNACK) + BUG_RULES
          + clues("x1c", [
              "Bug 1: the error names line 3. What type is the value of <code>count</code>?",
              "Bug 2: the program runs, but it prints the curly braces. Which letter is missing "
              "in front of the opening quote mark?",
              "Bug 3: the error says a name is not defined. Compare how that name is spelled with "
              "the name on line 1.",
          ]))
    if KEY["on"]:
        cc = bug_key(rows, s4)

    return [card("A", "build it from the steps", 15, "Silly story", a),
            card("B", "build it from the steps", 15, "Age calculator", b),
            card("C", "bug hunt", 15, "Bug hunt: the snack machine", cc, bug=True)]


# =================================================================== session 2

QUIZ = '''score = 0

answer = input("How many legs does a spider have? ")
if answer == "8":
    print("Correct.")
    score = score + 1
else:
    print("No. A spider has 8 legs.")

answer = input("What is the capital of France? ")
if answer == "Paris":
    print("Correct.")
    score = score + 1
else:
    print("No. It is Paris.")

answer = input("Which planet do we live on? ")
if answer == "Earth":
    print("Correct.")
    score = score + 1
else:
    print("No. It is Earth.")

if score == 3:
    print("Perfect. 3 out of 3.")
elif score == 2:
    print("Close. 2 out of 3.")
else:
    print(f"You got {score} out of 3. Run it again.")
'''
QUIZ_Q1 = "\n\n".join(QUIZ.split("\n\n")[:2]) + "\n"
OR_LINE = 'if answer == "Paris" or answer == "paris":'

GUESS_STARTER = '''secret = 37
guess = 0

while guess != secret:
    guess = input("Guess my number, 1 to 50: ")
    guess = int(guess)
    if guess < secret:
        print("Too low.")

print("You got it.")
'''
GUESS = edit(GUESS_STARTER, '        print("Too low.")\n',
             '        print("Too low.")\n    elif guess > secret:\n        print("Too high.")\n')
GUESS_MORE = edit(edit(edit(GUESS, "guess = 0\n", "guess = 0\ntries = 0\n"),
                       "    guess = int(guess)\n", "    guess = int(guess)\n    tries = tries + 1\n"),
                  'print("You got it.")\n',
                  'print(f"You got it in {tries} tries.")\n'
                  'if tries <= 4:\n    print("Sharp guessing.")\n'
                  'elif tries <= 7:\n    print("Not bad.")\n'
                  'else:\n    print("That took a while.")\n')

DOOR = '''age = input("Age: ")
ticket = input("Ticket? yes or no: ")
if age > 13 and ticket = "yes":
    print("Come in.")
else:
    print("Not today.")
'''
DOOR_ROWS = [("15", "yes", "Come in."), ("13", "yes", "Come in."),
             ("13", "no", "Not today."), ("10", "yes", "Not today.")]


def session2():
    n = 2
    # ---- card A
    assert QUIZ.startswith(QUIZ_Q1) and QUIZ_Q1.count("input(") == 1
    quiz_out = ok(QUIZ, ["8", "London", "Earth"], name=fname(n, "quiz"), tag="x2a")
    endings = {}
    for typed in (["8", "Paris", "Earth"], ["8", "London", "Earth"], ["9", "Rome", "Mars"]):
        endings[tuple(typed)] = ok(QUIZ, typed, name=fname(n, "quiz"), tag="x2a-endings").splitlines()[-1]
    assert len(set(endings.values())) == 3
    reset = edit(QUIZ, "\nif score == 3:", "\nscore = 0\nif score == 3:")
    reset_last = ok(reset, ["8", "Paris", "Earth"], name=fname(n, "quiz"), tag="x2a-reset").splitlines()[-1]
    assert reset_last == "You got 0 out of 3. Run it again."
    with_or = edit(QUIZ, 'if answer == "Paris":', OR_LINE)
    assert ok(with_or, ["8", "paris", "Earth"], name=fname(n, "quiz"), tag="x2a-or").splitlines()[-1] \
        == endings[("8", "Paris", "Earth")]
    half_or = edit(QUIZ, 'if answer == "Paris":', 'if answer == "Paris" or "paris":')
    assert "Correct." == ok(half_or, ["8", "London", "Earth"], name=fname(n, "quiz"),
                            tag="x2a-half-or").splitlines()[3]
    a = ("<p>You make a quiz that asks three questions, keeps score, and prints a different last "
         "line for 3 right, 2 right, and anything lower.</p>" + file_line(n, "quiz")
         + "<p>In this finished run the player got the second question wrong.</p>"
         + want(quiz_out)
         + "<p>Question 1 is done for you. Type it in.</p>" + render.code_block(QUIZ_Q1)
         + "<p>The 8 is in quote marks because <code>input</code> gives text, and this gate "
           "compares text with text. No <code>int()</code> is needed here.</p>"
         + steps([
             "Under question 1, write two more questions of your own. Each one has an "
             "<code>input</code> line and a gate, the same as question 1.",
             "After the third question, write a three-way gate on <code>score</code>. If "
             "<code>score</code> is 3, print <code>Perfect. 3 out of 3.</code> If <code>score</code> "
             "is 2, print <code>Close. 2 out of 3.</code> For anything else, print the score in an "
             "f-string.",
         ])
         + ask("x2a-before", "Before you run",
               "<code>score = 0</code> is on line 1, above all three questions. Suppose you added a "
               "second <code>score = 0</code> just above the last gate. A player gets all three "
               "right. What would the last line print?",
               c(reset_last) + " The second <code>score = 0</code> replaces the count just before "
               "the gate reads it.")
         + "<p><b>Check:</b> run it three times. Get all three right, then two right, then none "
           "right. You should see three different last lines.</p>"
           "<h3>Go further</h3><p>Pick a question whose answer is a word. A player who types the "
           "word without its capital letter is marked wrong. Change that gate so both spellings "
           "are correct. Use <code>or</code>, with a whole comparison on each side of it, like "
           "this:</p>" + render.code_block(OR_LINE))
    if KEY["on"]:
        a = (render.code_block(QUIZ) + want(quiz_out, "What it prints")
             + "<p><b>Before you run:</b> a second <code>score = 0</code> just above the last gate "
               "replaces the count, so every run ends with " + c(reset_last) + "</p>"
               "<p><b>Go further:</b> " + c(OR_LINE) + " Watch for "
             + c('if answer == "Paris" or "paris":') + " That version marks every answer correct. "
               "Let the student find that out by typing London.</p>")

    # ---- card B
    starter_out = ok(GUESS_STARTER, ["20", "40", "37"], name=fname(n, "guess"), tag="x2b-starter")
    sl = starter_out.splitlines()
    assert sl[2].endswith(": 40") and sl[3].endswith(": 37"), starter_out
    guess_out = ok(GUESS, ["20", "40", "35", "37"], name=fname(n, "guess"), tag="x2b")
    assert guess_out.splitlines()[3] == "Too high."
    more = ok(GUESS_MORE, ["20", "40", "35", "37"], name=fname(n, "guess"), tag="x2b-more").splitlines()
    assert more[-2:] == ["You got it in 4 tries.", "Sharp guessing."]
    b = ("<p>The program holds a secret number. The player keeps guessing until the guess is "
         "right. You get a starter that works but leaves one thing out.</p>" + file_line(n, "guess")
         + "<p>Type the starter:</p>" + render.code_block(GUESS_STARTER)
         + "<p>The gate is inside the while loop, so the <code>if</code> line is indented 4 spaces "
           "and its block is indented 8 spaces. The gate runs once on every pass of the loop.</p>"
         + ask("x2b-before", "Before you run",
               "Find the stopping condition. Which guess makes the loop stop?",
               "The condition is <code>guess != secret</code>. The loop stops when the guess is 37, "
               "because then <code>guess != secret</code> is False.")
         + "<p>Run the starter and guess 20, then 40, then 37.</p>"
         + want(starter_out, "What the starter prints")
         + "<p>After the guess of 40 the program prints nothing, so the player gets no help.</p>"
         + steps([
             "Add an <code>elif</code> under the <code>if</code>, lined up with it. When the guess "
             "is greater than the secret, print <code>Too high.</code>",
             "Run it again with 20, 40, 35, 37. It should print the finished run below.",
         ])
         + want(guess_out)
         + "<h3>Go further</h3><p><b>Part 1.</b> Count the guesses. Make a variable "
           "<code>tries = 0</code> above the loop. Add 1 to it inside the loop. Change the last "
           "line to an f-string, so that the same four guesses print " + c(more[-2]) + "</p>"
           "<p><b>Part 2.</b> After that line, add a three-way gate on <code>tries</code>. For 4 or "
           "fewer print <code>Sharp guessing.</code> For 7 or fewer print <code>Not bad.</code> For "
           "anything else print <code>That took a while.</code></p>")
    if KEY["on"]:
        b = ("<p><b>Before you run:</b> the stopping condition is <code>guess != secret</code>. "
             "The loop stops when the guess is 37.</p><p>This is the program with both Go further "
             "parts.</p>" + render.code_block(GUESS_MORE)
             + want("\n".join(more), "What it prints for 20, 40, 35, 37"))

    # ---- card C
    d2 = edit(DOOR, 'ticket = "yes"', 'ticket == "yes"')
    d3 = edit(d2, 'age = input("Age: ")\n', 'age = input("Age: ")\nage = int(age)\n')
    d4 = edit(d3, "age > 13", "age >= 13")
    for age, ticket, should in DOOR_ROWS:
        got3 = ok(d3, [age, ticket], name=fname(n, "bugs"), tag="x2c-bug3").splitlines()[-1]
        got4 = ok(d4, [age, ticket], name=fname(n, "bugs"), tag="x2c-final").splitlines()[-1]
        assert got4 == should, (age, ticket, got4)
        assert (got3 != should) == ((age, ticket) == ("13", "yes")), (age, ticket, got3)
    rows = bug_table(n, "bugs", [
        {"code": DOOR, "kind": "error", "expect": "SyntaxError", "line": 3,
         "bug": "One equals sign in a comparison", "fix": c('ticket == "yes"')},
        {"code": d2, "kind": "error", "line": 3,
         "expect": "'>' not supported between instances of 'str' and 'int'",
         "bug": "<code>age</code> is still text", "fix": "Add <code>age = int(age)</code> under line 1"},
        {"code": d3, "kind": "wrong", "typed": ["13", "yes"], "shows": ["Not today."],
         "sees": "13 and yes prints <code>Not today.</code>",
         "bug": c("age > 13") + " leaves out 13", "fix": c("age >= 13")},
        {"code": d4, "kind": "done", "typed": ["13", "yes"], "shows": ["Come in."],
         "sees": "All four rows of the table match"},
    ], ["15", "yes"], "x2c")
    cc = ("<p>A sign on a door says: you can come in if you are 13 or older and you have a "
          "ticket. This program is supposed to follow the sign. It has 3 bugs.</p>"
          + file_line(n, "bugs") + "<p>Type the program exactly as it is here, bugs and all:</p>"
          + render.code_block(DOOR)
          + "<p>Two of the bugs stop the program with an error. The third bug gives no error: "
            "the program runs and prints the wrong line for one of the four people in this "
            "table. Fix the first two bugs, one per run. Then run the program once for each row "
            "to find the third.</p>"
          + table(["Age", "Ticket", "It should print"],
                  [[r[0], r[1], c(r[2])] for r in DOOR_ROWS])
          + "<p>For each bug, write down the line number and what you changed.</p>"
          + clues("x2c", [
              "Bug 1: the error points at line 3. One equals sign stores a value. Two equals "
              "signs make a comparison.",
              "Bug 2: the error says <code>'&gt;' not supported between instances of 'str' and "
              "'int'</code>. Which variable is still text?",
              "Bug 3: test the row with 13 and yes. The sign says 13 or older. Which comparison "
              "means 13 or more?",
          ]))
    if KEY["on"]:
        cc = bug_key(rows, d4)

    return [card("A", "build it from the steps", 20, "Three-question quiz", a),
            card("B", "finish the starter", 15, "Guess my number", b),
            card("C", "bug hunt", 15, "Bug hunt: the door", cc, bug=True)]


# =================================================================== session 3

TABLE = '''n = input("Which times table? ")
n = int(n)

for i in range(1, 13):
    answer = n * i
    print(f"{n} x {i} = {answer}")
'''
TABLE_MORE = '''n = input("Which times table? ")
n = int(n)

total = 0
over_50 = 0
for i in range(1, 13):
    answer = n * i
    print(f"{n} x {i} = {answer}")
    total = total + answer
    if answer > 50:
        over_50 = over_50 + 1

print(f"The twelve answers add up to {total}.")
print(f"{over_50} of the answers are over 50.")
'''

COINS_STARTER = '''import random

sides = ["heads", "tails"]
heads = 0

for flip in range(1, 21):
    result = random.choice(sides)
    print(f"Flip {flip}: {result}")
    if result == "heads":
        heads = heads + 1

print(f"Heads: {heads}")
'''
COINS = edit(edit(edit(
    COINS_STARTER, "heads = 0\n\n", "heads = 0\ntails = 0\n\n"),
    "        heads = heads + 1\n\n",
    "        heads = heads + 1\n    else:\n        tails = tails + 1\n\n"),
    'print(f"Heads: {heads}")\n',
    'print(f"Heads: {heads}")\nprint(f"Tails: {tails}")\n'
    'if heads > tails:\n    print("Heads wins.")\n'
    'elif heads == tails:\n    print("A draw.")\n'
    'else:\n    print("Tails wins.")\n')
COINS_MORE = edit(edit(edit(edit(
    COINS, "tails = 0\n\n", "tails = 0\nrun = 0\nlongest = 0\n\n"),
    "        heads = heads + 1\n", "        heads = heads + 1\n        run = run + 1\n"),
    "        tails = tails + 1\n", "        tails = tails + 1\n        run = 0\n    if run > longest:\n        longest = run\n"),
    'print(f"Tails: {tails}")\n', 'print(f"Tails: {tails}")\nprint(f"Longest run of heads: {longest}")\n')
COINS_SEED = 4

SCORES = '''scores = [72, 95, 88, 97, 67]
best = 100
for s in scores:
    count = 0
    if s > 80:
        count = count + 1
    if s > best:
        best = s
print(f"over 80: {count}")
print(f"best: {best}")
print(f"last score: {scores[5]}")
'''
LOWEST = '''scores = [72, 95, 88, 97, 67]
lowest = 100
for s in scores:
    if s < lowest:
        lowest = s
print(f"lowest: {lowest}")
print(min(scores))
'''


def session3():
    n = 3
    # ---- card A
    table_out = ok(TABLE, ["7"], name=fname(n, "table"), tag="x3a")
    assert table_out.splitlines()[-1] == "7 x 12 = 84" and len(table_out.splitlines()) == 13
    more = ok(TABLE_MORE, ["7"], name=fname(n, "table"), tag="x3a-more").splitlines()
    assert more[-2] == "The twelve answers add up to %d." % sum(7 * i for i in range(1, 13))
    assert more[-1] == "%d of the answers are over 50." % sum(1 for i in range(1, 13) if 7 * i > 50)
    a = ("<p>You make a program that asks which times table the player wants, then prints that "
         "table from 1 to 12.</p>" + file_line(n, "table") + want(table_out)
         + steps([
             "Ask which times table. Store the answer in a variable called <code>n</code> and "
             "change its type to a number.",
             "Write a for loop with <code>range(1, 13)</code>. Call the loop variable <code>i</code>.",
             "Inside the loop, make a variable called <code>answer</code>. Its value is "
             "<code>n</code> times <code>i</code>.",
             "Still inside the loop, print one line of the table with an f-string. The x in the "
             "output is the letter x, typed inside the f-string.",
         ])
         + ask("x3a-before", "Before you run",
               "The table stops at 12. Why does the range say 13?",
               "<code>range(1, 13)</code> starts at 1 and stops before 13, so the last value of "
               "<code>i</code> is 12.")
         + "<h3>Go further</h3><p><b>Part 1.</b> Add up the twelve answers with an accumulator. "
           "After the loop, print the total. For the 7 times table it should print "
         + c(more[-2]) + "</p><p><b>Part 2.</b> Count how many of the twelve answers are over 50. "
           "Use a counter with a gate. For the 7 times table it should print " + c(more[-1]) + "</p>")
    if KEY["on"]:
        a = ("<p><b>Before you run:</b> <code>range</code> stops before its second number, so "
             "<code>range(1, 13)</code> gives 1 to 12.</p><p>This is the program with both Go "
             "further parts.</p>" + render.code_block(TABLE_MORE)
             + want("\n".join(more[-2:]), "Its last two lines for the 7 times table"))

    # ---- card B
    st = ok(COINS_STARTER, seed=COINS_SEED, name=fname(n, "coins"), tag="x3b-starter").splitlines()
    assert st[0] == "Flip 1: heads" and st[1] == "Flip 2: tails" and st[-1].startswith("Heads: "), st
    fin = ok(COINS, seed=COINS_SEED, name=fname(n, "coins"), tag="x3b").splitlines()
    assert fin[:20] == st[:20] and fin[20] == st[20], fin
    heads_n = int(fin[20].split(": ")[1])
    tails_n = int(fin[21].split(": ")[1])
    assert heads_n + tails_n == 20 and fin[22] == "Heads wins." and heads_n > tails_n, fin[20:]
    # every seed: the two counts add to 20 and the verdict matches them
    for seed in range(40):
        lines_ = ok(COINS, seed=seed, name=fname(n, "coins"), tag="x3b-seeds").splitlines()
        h = sum(1 for ln in lines_[:20] if ln.endswith("heads"))
        t = 20 - h
        assert lines_[20] == f"Heads: {h}" and lines_[21] == f"Tails: {t}", (seed, lines_[20:])
        right = "Heads wins." if h > t else "A draw." if h == t else "Tails wins."
        assert lines_[22] == right, (seed, lines_[20:])
    more = ok(COINS_MORE, seed=COINS_SEED, name=fname(n, "coins"), tag="x3b-more").splitlines()
    assert more[:22] == fin[:22] and more[-1] == fin[-1], more
    longest_n = int(more[22].split(": ")[1])
    run = best = 0
    for ln in more[:20]:
        run = run + 1 if ln.endswith("heads") else 0
        best = max(best, run)
    assert longest_n == best == 4, (longest_n, best)
    b = ("<p>The computer flips a coin twenty times with <code>random.choice</code> and prints "
         "each flip. You get a starter that runs but only counts one side.</p>" + file_line(n, "coins")
         + "<p>Type the starter:</p>" + render.code_block(COINS_STARTER)
         + "<p>The gate is inside the for loop, so the <code>if</code> line is indented 4 spaces "
           "and its block is indented 8 spaces. The gate runs once on every flip.</p>"
         + ask("x3b-before", "Before you run",
               "Look at the gate. On a flip that lands tails, which lines inside the loop run?",
               "The <code>result</code> line and the print line. The gate's condition is False for "
               "tails, so its block is skipped and nothing counts that flip.")
         + "<p>The flips are random, so your run will be different from this one.</p>"
         + want("\n".join(st[:3] + ["..."] + st[-2:]), "The start and end of one run of the starter")
         + "<p>The starter counts heads and nothing else. The tails count is missing, and so is "
           "the result.</p>"
         + steps([
             "Make a second counter, <code>tails = 0</code>, under <code>heads = 0</code>.",
             "Add an <code>else</code> to the gate, lined up with the <code>if</code>. In its "
             "block, add 1 to <code>tails</code>.",
             "After the loop, print the tails count the same way the heads count is printed.",
             "Under that, add a three-way gate on the two counters. More heads prints "
             "<code>Heads wins.</code> Equal prints <code>A draw.</code> Anything else prints "
             "<code>Tails wins.</code>",
         ])
         + want("\n".join(fin[20:]), "The last three lines of a finished run")
         + "<p><b>Check:</b> run it three times. Heads plus tails is 20 every time.</p>"
           "<h3>Go further</h3><p>Find the longest run of heads: the most times in a row the coin "
           "landed heads. You need two more counters above the loop, <code>run = 0</code> and "
           "<code>longest = 0</code>. Inside the heads block, add 1 to <code>run</code>. Inside "
           "the else block, set <code>run</code> back to 0, because a tails flip ends the run. "
           "Then, after the gate and still inside the loop, use best so far: if <code>run</code> "
           "is greater than <code>longest</code>, store <code>run</code> in <code>longest</code>. "
           "Print <code>longest</code> after the loop. For the run that printed the lines above, it is "
         + str(longest_n) + ". Your run will give its own number.</p>")
    if KEY["on"]:
        b = ("<p><b>Before you run:</b> on a tails flip, only the <code>result</code> line and the "
             "print line run. The gate's block is skipped.</p>" + render.code_block(COINS)
             + want("\n".join(fin[20:]), "The last three lines of one run")
             + "<p><b>Go further:</b> this is the program with the longest run of heads. "
               "<code>run</code> is a counter that is reset on purpose, and <code>longest</code> is "
               "best so far from chunk 5. For the seeded run on the card it prints "
             + str(longest_n) + ".</p>" + render.code_block(COINS_MORE)
             + "<p>If the student puts the <code>run = 0</code> line above the loop only, and never "
               "resets it, <code>longest</code> comes out equal to the heads count. Ask what should "
               "happen to the run when the coin lands tails.</p>")

    # ---- card C
    c2 = edit(SCORES, "scores[5]", "scores[4]")
    c3 = edit(c2, "best = 100\nfor s in scores:\n    count = 0\n", "best = 100\ncount = 0\nfor s in scores:\n")
    c4 = edit(c3, "best = 100", "best = 0")
    final_out = ok(c4, name=fname(n, "bugs"), tag="x3c-final")
    assert final_out.splitlines() == ["over 80: 3", "best: 97", "last score: 67"]
    low = ok(LOWEST, name=fname(n, "bugs"), tag="x3c-lowest").splitlines()
    assert low == ["lowest: 67", "67"]
    rows = bug_table(n, "bugs", [
        {"code": SCORES, "kind": "error", "expect": "IndexError", "line": 11,
         "shows": ["over 80: 0", "best: 100"],
         "bug": "Five items have indexes 0 to 4", "fix": c("scores[4]")},
        {"code": c2, "kind": "wrong", "shows": ["over 80: 0"],
         "bug": "<code>count = 0</code> is inside the loop, so it runs on every pass",
         "fix": "Move <code>count = 0</code> above the <code>for</code> line"},
        {"code": c3, "kind": "wrong", "shows": ["best: 100"],
         "bug": "No score is greater than 100, so <code>best</code> never changes",
         "fix": c("best = 0")},
        {"code": c4, "kind": "done", "shows": final_out.splitlines()},
    ], None, "x3c")
    cc = ("<p>This program has 3 bugs. It is supposed to print this:</p>" + want(final_out)
          + file_line(n, "bugs") + "<p>Type the program exactly as it is here, bugs and all:</p>"
          + render.code_block(SCORES)
          + "<p>One bug stops the program with an error. The other two give no error: the "
            "program runs and prints wrong numbers. You find those two by comparing your output "
            "with the finished run above.</p>"
          + "<p>Fix one thing per run. For each bug, write down the line number and what you "
            "changed.</p>"
          + clues("x3c", [
              "Bug 1: the error names line 11. The list has 5 items. What is the index of the "
              "last item?",
              "Bug 2: <code>over 80</code> prints 0. Look at where <code>count = 0</code> is. How "
              "many times does that line run?",
              "Bug 3: <code>best</code> prints 100, and no score in the list is 100. What starting "
              "value is lower than every score?",
          ])
          + "<h3>Go further</h3><p>Add a variable called <code>lowest</code> and find the lowest "
            "score with best so far. Print it. Then check it against <code>min(scores)</code>. "
            "Both should give " + low[1] + ".</p>")
    if KEY["on"]:
        cc = (bug_key(rows, c4, "The student may fix bugs 2 and 3 in either order.")
              + "<p><b>Go further:</b> <code>lowest = 100</code> above the loop, then "
                "<code>if s &lt; lowest:</code> with <code>lowest = s</code> in its block. It "
                "prints " + low[1] + ", the same as <code>min(scores)</code>. The starting value "
                "for <code>lowest</code> has to be higher than every score. For <code>best</code> "
                "it has to be lower than every score.</p>")

    return [card("A", "build it from the steps", 15, "Times table", a),
            card("B", "finish the starter", 20, "Coin flips", b),
            card("C", "bug hunt", 15, "Bug hunt: the score report", cc, bug=True)]


# =================================================================== session 5

GRADES = '''def grade_of(score):
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    return "not yet"

print(grade_of(95))
print(grade_of(80))
print(grade_of(42))

scores = [72, 95, 88, 97, 67]
for s in scores:
    grade = grade_of(s)
    print(f"{s} gets {grade}")
'''
COUNT_GRADE = '''def count_grade(scores, letter):
    count = 0
    for s in scores:
        if grade_of(s) == letter:
            count = count + 1
    return count
'''
GRADES_MORE = (edit(GRADES, '    return "not yet"\n\n', '    return "not yet"\n\n' + COUNT_GRADE + "\n")
               + '\nprint(count_grade(scores, "A"))\nprint(count_grade(scores, "B"))\n')

ROLL = '''import random

def roll():
    return random.choice([1, 2, 3, 4, 5, 6])
'''
DICE = ROLL + '''
def roll_two():
    return roll() + roll()

def winner_of(you, computer):
    if you > computer:
        return "you"
    if computer > you:
        return "computer"
    return "tie"

your_wins = 0
for round_number in range(1, 6):
    input("Press Enter to roll.")
    you = roll_two()
    computer = roll_two()
    result = winner_of(you, computer)
    print(f"Round {round_number}: you rolled {you}, the computer rolled {computer}. Winner: {result}")
    if result == "you":
        your_wins = your_wins + 1

print(f"You won {your_wins} of 5 rounds.")
'''
DICE_SEED = 0
ROLL_MANY = '''def roll_many(count):
    total = 0
    for i in range(count):
        total = total + roll()
    return total
'''

AVERAGE = '''print(average_of([12, 20, 28, 20]))

def total_of(numbers):
    total = 0
    for n in numbers:
        total = total + n
        return total

def average_of(numbers):
    print(total_of(numbers) / len(numbers))
'''


def session5():
    n = 5
    fare = [ch for ch in SESS[5]["chunks"] if "def fare(age):" in ch["code"]]
    assert len(fare) == 1, "card 5A points at fare(age) on the session 5 page"
    # ---- card A
    g_out = ok(GRADES, name=fname(n, "grades"), tag="x5a")
    assert g_out.splitlines()[:3] == ["A", "B", "not yet"]
    gm = ok(GRADES_MORE, name=fname(n, "grades"), tag="x5a-more").splitlines()
    count_a, count_b = gm[-2], gm[-1]
    assert gm[:-2] == g_out.splitlines() and (count_a, count_b) == ("2", "1")
    a = ("<p>You write a function called <code>grade_of</code> that takes a score and returns "
         "a grade. Then you use it on a whole list of scores.</p>"
         "<p>The rule: 90 or more returns <code>\"A\"</code>. 80 or more returns "
         "<code>\"B\"</code>. 70 or more returns <code>\"C\"</code>. Anything lower returns "
         "<code>\"not yet\"</code>.</p>" + file_line(n, "grades") + want(g_out)
         + steps([
             "At the top of the file, write <code>def grade_of(score):</code>. In its body, use "
             "flat gates with a <code>return</code> in each one, the same shape as "
             "<code>fare(age)</code> on the session 5 page.",
             "Under the function, at the left edge, test it with three lines: "
             "<code>print(grade_of(95))</code>, <code>print(grade_of(80))</code>, and "
             "<code>print(grade_of(42))</code>.",
             "Make the list <code>scores = [72, 95, 88, 97, 67]</code>.",
             "Loop through <code>scores</code>. On each pass, call <code>grade_of</code>, store "
             "the return value in a variable called <code>grade</code>, and print a line like "
             "<code>72 gets C</code> with an f-string.",
         ])
         + ask("x5a-before", "Before you run",
               "95 is 90 or more, and it is also 80 or more. Why does <code>grade_of(95)</code> "
               "return <code>\"A\"</code> and not <code>\"B\"</code>?",
               "<code>return</code> ends the function. 95 passes the first gate, the function "
               "returns <code>\"A\"</code>, and the gate for 80 never runs.")
         + "<h3>Go further</h3><p>Write a second function, <code>count_grade(scores, letter)</code>. "
           "It returns how many scores in the list get that grade. It has a counter and a loop, "
           "and it calls <code>grade_of</code> inside its gate. Put its <code>def</code> under "
           "<code>grade_of</code> and above the lines that print. With the list above, "
           "<code>count_grade(scores, \"A\")</code> returns " + count_a + " and "
           "<code>count_grade(scores, \"B\")</code> returns " + count_b + ".</p>")
    if KEY["on"]:
        a = ("<p><b>Before you run:</b> <code>return</code> ends the function. 95 passes the first "
             "gate, the function returns <code>\"A\"</code>, and the gate for 80 never runs.</p>"
             "<p>This is the program with the Go further part: <code>count_grade</code> and the "
             "last two lines.</p>" + render.code_block(GRADES_MORE)
             + want("\n".join(gm), "What it prints"))

    # ---- card B
    assert DICE.startswith(ROLL)
    d_out = ok(DICE, [""] * 5, DICE_SEED, fname(n, "dice"), "x5b")
    winners = re.findall(r"Winner: (\w+)", d_out)
    assert len(winners) == 5 and set(winners) == {"you", "computer", "tie"}, d_out
    for seed in range(60):
        for ln in ok(DICE, [""] * 5, seed, fname(n, "dice"), "x5b-fair").splitlines():
            m = re.match(r"Round \d: you rolled (\d+), the computer rolled (\d+)\. Winner: (\w+)", ln)
            if m:
                y, cpu = int(m.group(1)), int(m.group(2))
                assert 2 <= y <= 12 and 2 <= cpu <= 12
                assert m.group(3) == ("you" if y > cpu else "computer" if cpu > y else "tie")
    many = ok(ROLL + "\n" + ROLL_MANY + "\nfor k in range(200):\n    print(roll_many(10))\n",
              seed=1, name=fname(n, "dice"), tag="x5b-more")
    assert all(10 <= int(v) <= 60 for v in many.split())
    b = ("<p>You and the computer each roll two dice for five rounds. The higher total wins "
         "the round. You build the game from three small functions.</p>" + file_line(n, "dice")
         + "<p>The first function is done for you. It returns one random number from 1 to 6. "
           "Type it in:</p>" + render.code_block(ROLL)
         + steps([
             "Write <code>roll_two()</code>. It returns the total of two rolls. It calls "
             "<code>roll</code> twice and adds the two return values.",
             "Write <code>winner_of(you, computer)</code>. It returns <code>\"you\"</code> when the "
             "first number is higher, <code>\"computer\"</code> when the second number is higher, "
             "and <code>\"tie\"</code> when they are equal. Use flat gates and three returns.",
             "Under the three functions, at the left edge, make a counter "
             "<code>your_wins = 0</code>.",
             "Write a for loop with <code>range(1, 6)</code>. Inside it: the line "
             "<code>input(\"Press Enter to roll.\")</code>, then one call to <code>roll_two</code> "
             "for you, one call to <code>roll_two</code> for the computer, and one call to "
             "<code>winner_of</code>. Store all three return values.",
             "Still inside the loop, print the round with an f-string. Then add 1 to "
             "<code>your_wins</code> when the winner is <code>\"you\"</code>.",
             "After the loop, print how many rounds you won.",
         ])
         + "<p>The dice are random, so your numbers will be different from this finished run.</p>"
         + want(d_out)
         + ask("x5b-before", "Before you run",
               "What is the lowest number <code>roll_two()</code> can return, and what is the "
               "highest?",
               "The lowest is 2, from two rolls of 1. The highest is 12, from two rolls of 6.")
         + "<h3>Go further</h3><p>Write <code>roll_many(count)</code>. It returns the total of "
           "<code>count</code> rolls. Use an accumulator and a for loop with "
           "<code>range(count)</code>. Then print <code>roll_many(10)</code> a few times.</p>"
         + ask("x5b-more", "Question",
               "Every value <code>roll_many(10)</code> returns is between 10 and 60. Why?",
               "Ten rolls of 1 add up to 10, and ten rolls of 6 add up to 60. Every other set of "
               "ten rolls is in between."))
    if KEY["on"]:
        b = ("<p><b>Before you run:</b> the lowest is 2 and the highest is 12.</p>"
             + render.code_block(DICE) + want(d_out, "One run")
             + "<p><b>Go further:</b></p>" + render.code_block(ROLL_MANY)
             + "<p>Ten rolls of 1 add up to 10 and ten rolls of 6 add up to 60, so "
               "<code>roll_many(10)</code> is always between 10 and 60.</p>")

    # ---- card C
    body = AVERAGE.split("\n", 2)[2]
    v2 = body + "\n" + AVERAGE.split("\n", 1)[0] + "\n"
    v3 = edit(v2, "    print(total_of(numbers) / len(numbers))", "    return total_of(numbers) / len(numbers)")
    v4 = edit(v3, "        total = total + n\n        return total", "        total = total + n\n    return total")
    alt = edit(v2, "        total = total + n\n        return total", "        total = total + n\n    return total")
    final_out = ok(v4, name=fname(n, "bugs"), tag="x5c-final")
    assert final_out == "20.0"
    alt_out = ok(alt, name=fname(n, "bugs"), tag="x5c-alt").splitlines()
    assert alt_out == ["20.0", "None"]
    rows = bug_table(n, "bugs", [
        {"code": AVERAGE, "kind": "error", "expect": "NameError: name 'average_of' is not defined",
         "line": 1, "bug": "The call is above the <code>def</code>",
         "fix": "Move the <code>print</code> line to the bottom of the file"},
        {"code": v2, "kind": "wrong", "shows": ["3.0", "None"],
         "sees": "<code>3.0</code>, then <code>None</code>",
         "bug": "<code>average_of</code> prints the value and has no <code>return</code>",
         "fix": "In <code>average_of</code>, change <code>print(...)</code> to <code>return ...</code>"},
        {"code": v3, "kind": "wrong", "shows": ["3.0"],
         "bug": "<code>return total</code> is inside the loop, so <code>total_of</code> returns "
                "after the first number",
         "fix": "Move <code>return total</code> left by 4 spaces, so it lines up with <code>for</code>"},
        {"code": v4, "kind": "done", "shows": ["20.0"]},
    ], None, "x5c")
    cc = ("<p>This program has 3 bugs. The four numbers add up to 80, and 80 divided by 4 is "
          "20, so it is supposed to print this:</p>" + want(final_out)
          + file_line(n, "bugs") + "<p>Type the program exactly as it is here, bugs and all:</p>"
          + render.code_block(AVERAGE)
          + "<p>One bug stops the program with an error. The other two give no error: the "
            "program runs and prints the wrong thing.</p>"
          + "<p>Fix one thing per run. For each bug, write down the line number and what you "
            "changed.</p>"
          + clues("x5c", [
              "Bug 1: the error says <code>average_of</code> is not defined, and yet the "
              "<code>def</code> is in the file. Python reads a file from the top. Which does it "
              "reach first, the <code>def</code> or the call?",
              "Bug 2: the output has the word <code>None</code> in it. Which function prints a "
              "value when it should return the value?",
              "Bug 3: the output is 3.0, and 12 divided by 4 is 3. Why did <code>total_of</code> "
              "return only the first number? Look at how far the line <code>return total</code> "
              "is indented.",
          ]))
    if KEY["on"]:
        cc = bug_key(rows, v4, "The student may fix bugs 2 and 3 in either order. With the "
                     "indent fixed first, run 2 prints <code>" + alt_out[0] + "</code>, then <code>"
                     + alt_out[1] + "</code>.")

    return [card("A", "build it from the steps", 15, "Letter grades", a),
            card("B", "build it from the steps", 20, "Dice game", b),
            card("C", "bug hunt", 15, "Bug hunt: the average", cc, bug=True)]


BUILDERS = {1: session1, 2: session2, 3: session3, 5: session5}


# ------------------------------------------------------------- page furniture

def masthead(s, title, sub):
    return ('<header class="top"><div class="wrap">'
            '<p class="eyebrow">Beyond Vibe Coding &middot; Beginner &middot; Session '
            + str(s["num"]) + ' of 13</p><h1>' + esc(title) + '</h1>'
            '<p class="sub">' + sub + '</p><div class="dates">'
            '<span class="pill"><b>Monday section</b> ' + s["mon"] + '</span>'
            '<span class="pill"><b>Friday section</b> ' + s["fri"] + '</span>'
            '<span class="pill"><b>Cards</b> 3</span></div></div></header>')


def pager(s):
    nxt = SESS[s["num"] + 1]
    return ('<nav class="pager"><a href="' + render.link(s["slug"]) + '">&larr; Session '
            + str(s["num"]) + ': ' + esc(s["title"]) + '</a>'
            '<a href="' + render.link("beginner_semester_hub") + '">Course home</a>'
            '<a href="' + render.link(nxt["slug"]) + '">Session ' + str(nxt["num"]) + ': '
            + esc(nxt["title"]) + ' &rarr;</a></nav>')


def footer(s):
    return ('<footer><div class="wrap"><p>Beyond Vibe Coding, beginner semester, Fall 2026. '
            'Extra cards for session ' + str(s["num"]) + ', written by a generator in '
            '<code>build/</code>. Every finished run and every error message on these cards '
            'comes from running the program when the site was built.</p></div></footer>')


def titles(sections):
    return [html.unescape(t) for t in re.findall(r"<h2>(.*?)</h2>", "".join(sections))]


def cards_page(s):
    """Return the student's card page for one session."""
    n = s["num"]
    sections = BUILDERS[n]()
    assert titles(sections) == s["extras"]["cards"], (n, titles(sections))
    b = masthead(s, "Extra cards: three more programs",
                 "For when you finish the build with time left. Each card uses only what is on "
                 "the session " + str(n) + " page.")
    b += '<main><div class="wrap">'
    b += ('<div class="toolbar"><a class="btn quiet" href="' + render.link(s["slug"])
          + '">Back to the session ' + str(n) + ' page</a></div>')
    b += ('<section><h2>How the cards work</h2><ul>'
          '<li>Pick any one card. The three cards do not depend on each other.</li>'
          '<li>Each card needs a new file. The card gives the file name.</li>'
          '<li>Say what you think the program will do before you run it.</li>'
          '<li>Change one thing, then run it. One change per run.</li></ul></section>')
    b += "".join(sections)
    return b + '</div></main>' + pager(s) + footer(s)


def key_page(s):
    """Return the teacher's answer key for one session: the same cards with KEY on."""
    n = s["num"]
    KEY["on"] = True
    try:
        sections = BUILDERS[n]()
    finally:
        KEY["on"] = False
    b = masthead(s, "Extra cards: answer key",
                 "Teacher copy. The finished program for each card, what it prints, and the bugs "
                 "in the order a student meets them.")
    b += '<main><div class="wrap">'
    b += ('<div class="toolbar"><a class="btn quiet" href="' + render.link(s["slug"])
          + '">Back to the session ' + str(n) + ' page</a><a class="btn quiet" href="'
          + render.link(s["extras"]["slug"]) + '">The cards</a></div>')
    b += "".join(sections)
    return b + '</div></main>' + pager(s) + footer(s)
