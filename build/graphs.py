"""Figures for session 4: the rules of rock paper scissors drawn as arrows.

Each figure is an inline SVG in the Lecture Light palette. A node is one move and an
arrow points from the move that wins to the move it beats, with the rule's own verb
on the arrow. Nothing here is a photograph or a drawing of a character: the moves are
labelled circles, so the figures project cleanly and print on one sheet.
"""

import math

INK = "#17181B"
SOFT = "#4A4D53"
TEAL = "#0E4D52"
CLAY = "#9C2B22"
GREEN = "#1D5B39"
OCHRE = "#8A5A00"
CARD = "#FFFDF7"
RULE = "#D3CBB8"
FONT = "font-family:JetBrains Mono,monospace"

NODE_R = 50


def _seg_dist(p, a, b):
    """Distance from point p to the segment a-b."""
    (px, py), (ax, ay), (bx, by) = p, a, b
    dx, dy = bx - ax, by - ay
    if dx == dy == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def _trim(a, b):
    """The visible part of the arrow from node a to node b: start and end points."""
    (ax, ay), (bx, by) = a, b
    dx, dy = bx - ax, by - ay
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    return (ax + ux * (NODE_R + 4), ay + uy * (NODE_R + 4)), (bx - ux * (NODE_R + 12), by - uy * (NODE_R + 12))


def _crosses_box(seg, x0, y0, x1, y1):
    """True when the segment passes through the box (Liang-Barsky clipping)."""
    (ax, ay), (bx, by) = seg
    dx, dy = bx - ax, by - ay
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, ax - x0), (dx, x1 - ax), (-dy, ay - y0), (dy, y1 - ay)):
        if p == 0:
            if q < 0:
                return False
            continue
        r = q / p
        if p < 0:
            if r > t1:
                return False
            t0 = max(t0, r)
        else:
            if r < t0:
                return False
            t1 = min(t1, r)
    return t0 <= t1


def _box_room(cx, cy, hw, hh, others, nodes, taken):
    """How much clear space a label box centered at (cx, cy) has around it.

    Measured from the box's edges: to every other arrow, to every node's edge, and to
    every label already placed. Negative means something overlaps the box.
    """
    pts = [(cx + dx, cy + dy) for dx in (-hw, 0, hw) for dy in (-hh, 0, hh)]
    room = min(_seg_dist(p, *o) for p in pts for o in others)
    for o in others:
        if _crosses_box(o, cx - hw, cy - hh, cx + hw, cy + hh):
            room = min(room, -40.0)
    room = min([room] + [math.hypot(px - nx, py - ny) - NODE_R for px, py in pts for nx, ny in nodes])
    for qx, qy, qw, qh in taken:
        room = min(room, max(abs(cx - qx) - (hw + qw), abs(cy - qy) - (hh + qh)))
    return room


def _label_spot(a, b, others, nodes, taken, label):
    """Where on the arrow a-b its label box sits: the point with the most room.

    The box is centered on the arrow itself, so the arrow runs into one side of it and
    out of the other and there is no doubt which arrow the word belongs to. Among the
    points along the arrow, pick the one whose box is farthest from every other arrow,
    every node, and every label already placed. The tail half is tried first, so the
    word reads soon after the move that wins; the head half is used only when the tail
    half has no room.
    """
    (sx, sy), (ex, ey) = _trim(a, b)
    hw, hh = len(label) * 4.3 + 6, 11
    best, best_room, best_pt = 0.3, -1e9, None
    for lo, hi, penalty in ((10, 44, 0), (56, 90, 14)):
        for k in range(lo, hi + 1):
            t = k / 100.0
            px, py = sx + (ex - sx) * t, sy + (ey - sy) * t
            room = _box_room(px, py, hw, hh, others, nodes, taken) - penalty
            if room > best_room + 1e-6:
                best, best_room, best_pt = t, room, (px, py)
    taken.append((best_pt[0], best_pt[1], hw, hh))
    return best


def _arrow(a, b, label, color, t=0.5):
    """One arrow from node a to node b, trimmed to the circle edges, with its label on it."""
    (sx, sy), (ex, ey) = _trim(a, b)
    lx, ly = sx + (ex - sx) * t, sy + (ey - sy) * t
    w = len(label) * 8.6 + 12
    return (
        f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{color}" '
        f'stroke-width="4" marker-end="url(#head-{color[1:]})"/>'
        f'<rect x="{lx - w / 2:.1f}" y="{ly - 11:.1f}" width="{w:.1f}" height="22" rx="4" '
        f'fill="{CARD}" stroke="{color}" stroke-width="1.5"/>'
        f'<text x="{lx:.1f}" y="{ly + 5:.1f}" fill="{color}" font-weight="700" font-size="14" '
        f'text-anchor="middle">{label}</text>'
    )


def _node(x, y, label):
    return (
        f'<circle cx="{x}" cy="{y}" r="{NODE_R}" fill="{CARD}" stroke="{TEAL}" stroke-width="4"/>'
        f'<text x="{x}" y="{y + 6}" fill="{INK}" font-weight="700" font-size="17" '
        f'text-anchor="middle">{label}</text>'
    )


def _defs(colors):
    heads = "".join(
        f'<marker id="head-{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" '
        f'markerHeight="5" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" '
        f'fill="{c}"/></marker>' for c in colors)
    return "<defs>" + heads + "</defs>"


def rps_graph():
    """Three moves, three arrows: each move beats exactly one and loses to exactly one."""
    rock = (280, 70)
    scissors = (440, 300)
    paper = (120, 300)
    body = _defs([TEAL])
    body += _arrow(rock, scissors, "crushes", TEAL)
    body += _arrow(scissors, paper, "cuts", TEAL)
    body += _arrow(paper, rock, "covers", TEAL)
    body += _node(*rock, "rock") + _node(*scissors, "scissors") + _node(*paper, "paper")
    body += (f'<text x="20" y="372" fill="{SOFT}" font-size="14" font-weight="700">'
             'each word sits on its own arrow, which points from the move that wins to the move it beats</text>')
    return ('<h3>The rules as arrows</h3>'
            '<svg viewBox="0 0 560 390" width="100%" role="img" aria-label="Three circles '
            'labelled rock, paper, and scissors. An arrow from rock to scissors says crushes, '
            'an arrow from scissors to paper says cuts, and an arrow from paper to rock says '
            'covers. Each move has one arrow going out and one coming in." '
            f'style="max-width:560px;display:block;margin:0 0 16px;{FONT}">' + body + '</svg>')


def rpsls_graph():
    """Five moves, ten arrows: each move beats two and loses to two."""
    cx, cy, r = 320, 284, 200
    names = ["scissors", "paper", "rock", "lizard", "spock"]
    pos = {}
    for i, name in enumerate(names):
        ang = math.radians(-90 + i * 72)
        pos[name] = (round(cx + r * math.cos(ang)), round(cy + r * math.sin(ang)))
    ring = [("scissors", "paper", "cuts"), ("paper", "rock", "covers"),
            ("rock", "lizard", "crushes"), ("lizard", "spock", "poisons"),
            ("spock", "scissors", "smashes")]
    # the five crossing arrows make a star; each label sits on its own arrow at the
    # point with the most room, so it never lands on a crossing
    star = [("scissors", "lizard", "decapitates"), ("lizard", "paper", "eats"),
            ("paper", "spock", "disproves"), ("spock", "rock", "vaporizes"),
            ("rock", "scissors", "crushes")]
    segs = {(a, b): _trim(pos[a], pos[b]) for a, b, _ in ring + star}
    centers = list(pos.values())
    taken = []
    body = _defs([TEAL, CLAY])
    for a, b, verb in ring:
        (sx, sy), (ex, ey) = segs[(a, b)]
        taken.append(((sx + ex) / 2, (sy + ey) / 2, len(verb) * 4.3 + 6, 11))
        body += _arrow(pos[a], pos[b], verb, TEAL)
    for a, b, verb in sorted(star, key=lambda s: -len(s[2])):
        others = [s for k, s in segs.items() if k != (a, b)]
        t = _label_spot(pos[a], pos[b], others, centers, taken, verb)
        body += _arrow(pos[a], pos[b], verb, CLAY, t)
    for name in names:
        body += _node(*pos[name], name)
    body += (f'<text x="20" y="522" fill="{SOFT}" font-size="14" font-weight="700">'
             'each word sits on its own arrow, which points from the move that wins</text>'
             f'<text x="20" y="542" fill="{SOFT}" font-size="14" font-weight="700">'
             'to the move it beats: five round the outside, five across the middle</text>')
    return ('<h3>The ten rules as arrows</h3>'
            '<svg viewBox="0 0 640 556" width="100%" role="img" aria-label="Five circles in a '
            'ring labelled scissors, paper, rock, lizard, and spock. Five arrows go round the '
            'outside: scissors cuts paper, paper covers rock, rock crushes lizard, lizard '
            'poisons spock, spock smashes scissors. Five arrows cross the middle: scissors '
            'decapitates lizard, lizard eats paper, paper disproves spock, spock vaporizes '
            'rock, rock crushes scissors. Every circle has two arrows going out and two '
            f'coming in." style="max-width:640px;display:block;margin:0 0 16px;{FONT}">'
            + body + '</svg>')


def pairs_tree():
    """Player 1 picks one of three; for each, player 2 has two picks that are not a tie."""
    left = [("rock", 95), ("paper", 215), ("scissors", 335)]
    right = {"rock": ["paper", "scissors"], "paper": ["rock", "scissors"],
             "scissors": ["rock", "paper"]}
    body = (f'<text x="60" y="30" fill="{TEAL}" font-weight="700" font-size="15">you type</text>'
            f'<text x="330" y="30" fill="{TEAL}" font-weight="700" font-size="15">the computer picks</text>'
            f'<text x="520" y="30" fill="{TEAL}" font-weight="700" font-size="15">result</text>')
    beats = {("rock", "scissors"), ("paper", "rock"), ("scissors", "paper")}
    k = 0
    for name, y in left:
        body += (f'<rect x="20" y="{y - 20}" width="130" height="40" rx="6" fill="{CARD}" '
                 f'stroke="{TEAL}" stroke-width="3"/>'
                 f'<text x="85" y="{y + 6}" fill="{INK}" font-weight="700" font-size="16" '
                 f'text-anchor="middle">{name}</text>')
        for j, other in enumerate(right[name]):
            yy = y - 25 + j * 50
            body += (f'<line x1="150" y1="{y}" x2="300" y2="{yy}" stroke="{RULE}" stroke-width="3"/>'
                     f'<rect x="300" y="{yy - 18}" width="130" height="36" rx="6" fill="{CARD}" '
                     f'stroke="{OCHRE}" stroke-width="3"/>'
                     f'<text x="365" y="{yy + 6}" fill="{INK}" font-weight="700" font-size="16" '
                     f'text-anchor="middle">{other}</text>')
            win = (name, other) in beats
            body += (f'<text x="520" y="{yy + 6}" fill="{GREEN if win else CLAY}" font-weight="700" '
                     f'font-size="15">{"you win" if win else "you lose"}</text>')
            k += 1
    body += (f'<text x="20" y="396" fill="{SOFT}" font-size="14" font-weight="700">'
             '3 moves for you, times 2 computer moves that are not a tie, is 6 pairs.</text>'
             f'<text x="20" y="416" fill="{SOFT}" font-size="14" font-weight="700">'
             'Add the 3 ties for 9.</text>')
    return ('<h3>Every way a round can go, ties left out</h3>'
            '<svg viewBox="0 0 640 432" width="100%" role="img" aria-label="A tree. On the '
            'left, three boxes: rock, paper, scissors, for the move you type. From each box, '
            'two lines go to the two computer moves that are not a tie, and each pair is '
            'labelled you win or you lose. Three times two is six pairs; with the three ties '
            f'there are nine." style="max-width:640px;display:block;margin:0 0 16px;{FONT}">'
            + body + '</svg>')
