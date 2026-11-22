"""Bezier alphabet A-Z for turtle.

Coordinate system: x right, y UP (same as turtle). Every letter lives in a cell
60 wide and 100 tall, origin at the bottom-left corner of the cell.

A stroke is a list of cubic segments. A segment is (p0, p1, p2, p3).
Straight lines are stored as cubics too, so one drawing routine handles everything.
"""
import math

W = 60    # letter cell width
H = 100   # cap height
KAPPA_STEPS = 16  # turtle steps per cubic segment


# ---------------------------------------------------------------- builders
def line(a, b):
    """Straight line a->b as one cubic segment."""
    ax, ay = a
    bx, by = b
    return [(a,
             (ax + (bx - ax) / 3, ay + (by - ay) / 3),
             (ax + 2 * (bx - ax) / 3, ay + 2 * (by - ay) / 3),
             b)]


def poly(*pts):
    """Connected straight lines through the points."""
    segs = []
    for a, b in zip(pts, pts[1:]):
        segs += line(a, b)
    return segs


def arc(cx, cy, rx, ry, start_deg, end_deg):
    """Elliptical arc as cubic segments, split into pieces of at most 90 degrees.
    Positive span goes counterclockwise, negative goes clockwise."""
    span = end_deg - start_deg
    n = max(1, math.ceil(abs(span) / 90))
    step = math.radians(span / n)
    k = 4 / 3 * math.tan(step / 4)
    segs = []
    for i in range(n):
        a = math.radians(start_deg) + i * step
        b = a + step
        p0 = (cx + rx * math.cos(a), cy + ry * math.sin(a))
        p3 = (cx + rx * math.cos(b), cy + ry * math.sin(b))
        p1 = (p0[0] - k * rx * math.sin(a), p0[1] + k * ry * math.cos(a))
        p2 = (p3[0] + k * rx * math.sin(b), p3[1] - k * ry * math.cos(b))
        segs.append((p0, p1, p2, p3))
    return segs


# ---------------------------------------------------------------- letters
# Each letter: list of strokes. A stroke is a list of cubic segments.
LETTERS = {
    "A": [poly((0, 0), (30, 100), (60, 0)),
          line((12, 40), (48, 40))],

    "B": [line((0, 0), (0, 100)),
          line((0, 100), (30, 100)) + arc(30, 75, 25, 25, 90, -90) + line((30, 50), (0, 50)),
          line((0, 50), (32, 50)) + arc(32, 25, 28, 25, 90, -90) + line((32, 0), (0, 0))],

    "C": [arc(30, 50, 30, 50, 40, 320)],

    "D": [line((0, 0), (0, 100)),
          line((0, 100), (20, 100)) + arc(20, 50, 40, 50, 90, -90) + line((20, 0), (0, 0))],

    "E": [poly((55, 100), (0, 100), (0, 0), (55, 0)),
          line((0, 50), (45, 50))],

    "F": [poly((55, 100), (0, 100), (0, 0)),
          line((0, 55), (45, 55))],

    "G": [arc(30, 50, 30, 50, 40, 360) + line((60, 50), (34, 50))],

    "H": [line((0, 0), (0, 100)),
          line((60, 0), (60, 100)),
          line((0, 50), (60, 50))],

    "I": [line((30, 0), (30, 100)),
          line((10, 100), (50, 100)),
          line((10, 0), (50, 0))],

    "J": [line((45, 100), (45, 30)) + arc(22.5, 30, 22.5, 30, 0, -180),
          line((25, 100), (60, 100))],

    "K": [line((0, 0), (0, 100)),
          line((55, 100), (0, 40)),
          line((17, 58.5), (58, 0))],

    "L": [poly((0, 100), (0, 0), (55, 0))],

    "M": [poly((0, 0), (0, 100), (30, 40), (60, 100), (60, 0))],

    "N": [poly((0, 0), (0, 100), (60, 0), (60, 100))],

    "O": [arc(30, 50, 30, 50, 90, 450)],

    "P": [line((0, 0), (0, 100)),
          line((0, 100), (30, 100)) + arc(30, 72, 28, 28, 90, -90) + line((30, 44), (0, 44))],

    "Q": [arc(30, 50, 30, 50, 90, 450),
          line((38, 22), (62, -8))],

    "R": [line((0, 0), (0, 100)),
          line((0, 100), (30, 100)) + arc(30, 72, 28, 28, 90, -90) + line((30, 44), (0, 44)),
          line((30, 44), (60, 0))],

    # two arcs that meet at (30, 50) with the same tangent direction
    "S": [arc(30, 75, 28, 25, 30, 270) + arc(30, 25, 30, 25, 90, -150)],

    "T": [line((0, 100), (60, 100)),
          line((30, 100), (30, 0))],

    "U": [line((0, 100), (0, 30)) + arc(30, 30, 30, 30, 180, 360) + line((60, 30), (60, 100))],

    "V": [poly((0, 100), (30, 0), (60, 100))],

    "W": [poly((0, 100), (15, 0), (30, 70), (45, 0), (60, 100))],

    "X": [line((0, 0), (60, 100)),
          line((0, 100), (60, 0))],

    "Y": [poly((0, 100), (30, 50), (60, 100)),
          line((30, 50), (30, 0))],

    "Z": [poly((0, 100), (60, 100), (0, 0), (60, 0))],
}


# ---------------------------------------------------------------- math (pure)
def bezier(p0, p1, p2, p3, t):
    u = 1 - t
    return (
        u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0],
        u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1],
    )


def stroke_points(stroke, steps=KAPPA_STEPS):
    """Flatten a stroke into a list of (x, y) points in letter space."""
    pts = [stroke[0][0]]
    for seg in stroke:
        for i in range(1, steps + 1):
            pts.append(bezier(*seg, i / steps))
    return pts


def place(pts, origin, scale):
    ox, oy = origin
    return [(ox + x * scale, oy + y * scale) for x, y in pts]


def text_layout(text, origin=(0, 0), scale=1.0, gap=20):
    """Yield (char, letter_origin) for every drawable character.
    Spaces advance the cursor; unknown characters are skipped."""
    x, y = origin
    for ch in text.upper():
        if ch == " ":
            x += (W + gap) * scale
        elif ch in LETTERS:
            yield ch, (x, y)
            x += (W + gap) * scale


# ---------------------------------------------------------------- turtle drawing
def draw_stroke(pen, stroke, origin, scale):
    pts = place(stroke_points(stroke), origin, scale)
    pen.penup()
    pen.goto(pts[0])
    pen.pendown()
    for p in pts[1:]:
        pen.goto(p)
    pen.penup()  # never leave the pen down between strokes


def draw_text(pen, text, origin=(0, 0), scale=1.0, gap=20):
    for ch, o in text_layout(text, origin, scale, gap):
        for stroke in LETTERS[ch]:
            draw_stroke(pen, stroke, o, scale)


def main():
    import turtle
    screen = turtle.Screen()
    screen.setup(1100, 500)
    screen.tracer(0)  # draw instantly, then update once
    pen = turtle.Turtle(visible=False)
    pen.pensize(3)

    scale = 0.9
    row1 = "ABCDEFGHIJKLM"
    row2 = "NOPQRSTUVWXYZ"
    step = (W + 20) * scale
    x0 = -len(row1) * step / 2
    draw_text(pen, row1, (x0, 30), scale)
    draw_text(pen, row2, (x0, -130), scale)

    screen.update()
    screen.mainloop()


if __name__ == "__main__":
    main()
