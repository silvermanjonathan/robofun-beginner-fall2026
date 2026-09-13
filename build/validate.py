import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.environ.get("BVC_OUT", os.path.dirname(HERE))
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
BANNED_WORDS = ["genuinely", "delve", "tapestry", "testament to", "at its core",
                "dial worth turning", "earns its keep", "unleash", "supercharge",
                # locked decision 7: no page references a camp or another course
                "summer", "camp", "last term", "previous term"]
FAILURES = []
NOTES = []


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append("closing </%s> with nothing open at %s" % (tag, self.getpos()))
            return
        open_tag, pos = self.stack.pop()
        if open_tag != tag:
            self.errors.append("expected </%s> (opened %s) but found </%s> at %s"
                               % (open_tag, pos, tag, self.getpos()))


def check(name, text, all_names):
    fail = []

    p = Balance()
    p.feed(text)
    p.close()
    for e in p.errors:
        fail.append("tag balance: " + e)
    if p.stack:
        fail.append("unclosed tags: " + ", ".join(t for t, _ in p.stack))

    buttons = re.findall(r'<button class="rev" data-target="([^"]+)"', text)
    answers = re.findall(r'<div class="ans" id="([^"]+)">', text)
    if sorted(buttons) != sorted(answers):
        fail.append("reveal parity: %d buttons, %d answer blocks; unmatched %s"
                    % (len(buttons), len(answers),
                       set(buttons) ^ set(answers)))
    if len(set(buttons)) != len(buttons):
        fail.append("duplicate reveal ids")
    # every reveal button names the block it controls and starts collapsed
    controls = re.findall(r'<button class="rev" data-target="([^"]+)" aria-controls="([^"]+)" '
                          r'aria-expanded="false"', text)
    if len(controls) != len(buttons) or any(a != b for a, b in controls):
        fail.append("reveal buttons missing aria-controls/aria-expanded or mismatched target")

    # an input() prompt captured with nothing typed after it means stdin was not echoed
    for block in re.findall(r'<pre class="out">(.*?)</pre>', text, re.S):
        for ln in block.splitlines():
            if re.search(r'\?: ?$', ln.rstrip()) and ln.strip():
                fail.append("output box shows a prompt with no typed answer: " + ln.strip()[:60])

    # teacher panel timing rows must sum to exactly 90 minutes
    rows = re.findall(r'<li>\d+:\d\d [^<]*?, (\d+) min', text)
    if rows and sum(int(r) for r in rows) != 90:
        fail.append("timing rows sum to %d minutes, not 90" % sum(int(r) for r in rows))
    if rows and not re.search(r'<li>\d+:\d\d [^<]*ledger[^<]*, \d+ min', text):
        fail.append("teacher panel has no ledger stamp row")

    for block in re.findall(r'<pre[^>]*>(.*?)</pre>', text, re.S):
        if re.search(r'<(?!/?(?:code|b|em|span)\b)[a-zA-Z/]', block):
            fail.append("unescaped angle bracket inside a pre block: "
                        + block[:60].replace("\n", " "))

    for api in ("localStorage", "sessionStorage", "indexedDB"):
        if api in text:
            fail.append("storage API present: " + api)

    dashes = text.count("\u2014") + text.count("\u2013")
    if dashes:
        fail.append("dash characters found: %d" % dashes)

    low = text.lower()
    for w in BANNED_WORDS:
        if w in low:
            fail.append("banned phrase: " + w)

    for href in re.findall(r'href="([^"]+)"', text):
        if href.startswith("http") or href.startswith("#"):
            continue
        target = href.split("?")[0]
        if target not in all_names:
            fail.append("dead link: " + href)

    if "<h1>" not in text:
        fail.append("no h1")
    if "<title>" not in text:
        fail.append("no title")

    return fail


def main():
    names = sorted(f for f in os.listdir(SITE) if f.endswith(".html"))
    for n in names:
        text = open(os.path.join(SITE, n)).read()
        fails = check(n, text, set(names))
        status = "PASS" if not fails else "FAIL"
        kb = len(text) / 1024.0
        print("%-44s %s  %6.1f kB" % (n, status, kb))
        for f in fails:
            print("      -> " + f)
            FAILURES.append(n + ": " + f)

    print("\nfiles: %d" % len(names))
    revs = sum(len(re.findall(r'<button class="rev"', open(os.path.join(SITE, n)).read()))
               for n in names)
    outs = sum(len(re.findall(r'<pre class="out">', open(os.path.join(SITE, n)).read()))
               for n in names)
    print("reveal buttons: %d" % revs)
    print("verified output blocks: %d" % outs)
    if FAILURES:
        print("\n%d FAILURES" % len(FAILURES))
        sys.exit(1)
    print("\nall checks passed")


if __name__ == "__main__":
    main()
