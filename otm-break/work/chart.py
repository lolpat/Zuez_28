"""Synthetic example charts for "The Trendline Break" (not real market data). A price path is drawn through hand-placed
pivots (index, price 0-100) and turned into candles with seeded noise. Pivot highs and lows are hit exactly, so the wave
labels, the trend line and the channel sit on real candles.

Coordinates: price 0-100 maps to y BOT..TOP, candle index 0..NX maps to x X0..X1."""
import random

X0, X1, TOP, BOT = 80, 1000, 600, 1240


class Chart:
    def __init__(self, pivots, nx, seed, noise=1.6, pmin=0, pmax=100, top=TOP, bot=BOT, x0=X0, x1=X1):
        self.pv, self.nx, self.pmin, self.pmax = pivots, nx, pmin, pmax
        self.top, self.bot, self.x0, self.x1 = top, bot, x0, x1
        r = random.Random(seed)
        n = pivots[-1][0] + 1
        # target close per index: linear between pivots plus a little wobble
        path = []
        for (i0, p0), (i1, p1) in zip(pivots, pivots[1:]):
            for i in range(i0, i1):
                f = (i - i0) / (i1 - i0)
                path.append(p0 + (p1 - p0) * f)
        path.append(pivots[-1][1])
        piv = {i: p for i, p in pivots}
        kind = {}
        for k, (i, p) in enumerate(pivots):
            prev = pivots[k - 1][1] if k else None
            nxt = pivots[k + 1][1] if k + 1 < len(pivots) else None
            hi = (prev is None or p > prev) and (nxt is None or p > nxt)
            lo = (prev is None or p < prev) and (nxt is None or p < nxt)
            kind[i] = "hi" if hi else "lo" if lo else "mid"
        self.c = []
        prev_close = path[0]
        for i in range(n):
            close = path[i] + (r.uniform(-noise, noise) if i not in piv else 0)
            o = prev_close
            if i in piv and kind[i] == "hi":
                o = path[i] - r.uniform(0.6, 1.6); close = path[i] - r.uniform(0.2, 0.8)
            if i in piv and kind[i] == "lo":
                o = path[i] + r.uniform(0.6, 1.6); close = path[i] + r.uniform(0.2, 0.8)
            h = max(o, close) + r.uniform(0.3, noise * 0.9)
            lo = min(o, close) - r.uniform(0.3, noise * 0.9)
            if i in piv and kind[i] == "hi": h = path[i]
            if i in piv and kind[i] == "lo": lo = path[i]
            # keep every other candle inside the pivots' extremes nearby, so a pivot stays the local extreme
            for j in (i - 1, i + 1):
                if j in piv and kind[j] == "hi": h = min(h, piv[j] - 0.2); o = min(o, h); close = min(close, h)
                if j in piv and kind[j] == "lo": lo = max(lo, piv[j] + 0.2); o = max(o, lo); close = max(close, lo)
            self.c.append((o, h, lo, close))
            prev_close = close

    def cap_below(self, a, b, i0, i1, gap=0.4):
        """keep candles i0..i1-1 under the line through a and b (so the line is touched, not pierced, before the break)"""
        for i in range(i0, i1):
            o, h, lo, c = self.c[i]
            m = line_at(a, b, i) - (0 if i in (a[0], b[0]) else gap)
            h = min(h, m); o = min(o, h); c = min(c, h); lo = min(lo, min(o, c))
            self.c[i] = (o, h, lo, c)

    def x(self, i): return self.x0 + (self.x1 - self.x0) * i / self.nx
    def y(self, p): return self.bot - (self.bot - self.top) * (p - self.pmin) / (self.pmax - self.pmin)
    def xy(self, i, p): return (round(self.x(i), 1), round(self.y(p), 1))

    def candles(self, i0=0, i1=None, up="#e9ecf1", down="#7f8798", bw=None):
        """svg for candles i0..i1-1, one <g> per candle so they can be revealed in order"""
        i1 = len(self.c) if i1 is None else i1
        sp = (self.x1 - self.x0) / self.nx
        bw = bw or max(3.0, sp * 0.74)
        out = []
        for i in range(i0, i1):
            o, h, lo, c = self.c[i]
            col = up if c >= o else down
            x = self.x(i)
            yt, yb = self.y(max(o, c)), self.y(min(o, c))
            out.append(f'<line x1="{x:.1f}" y1="{self.y(h):.1f}" x2="{x:.1f}" y2="{self.y(lo):.1f}" stroke="{col}" stroke-width="1.6"/>'
                       f'<rect x="{x - bw / 2:.1f}" y="{yt:.1f}" width="{bw:.1f}" height="{max(1.5, yb - yt):.1f}" fill="{col}"/>')
        return out


def line_at(a, b, i):
    """price on the straight line through pivots a=(i, p) and b=(i, p) at index i"""
    return a[1] + (b[1] - a[1]) * (i - a[0]) / (b[0] - a[0])


# ---- the daily example: impulse 1-5, then W X Y X Z inside a falling channel, then a break of the trend line
DAILY = [(0, 10), (7, 26), (11, 19), (26, 62), (31, 53), (40, 86),                       # 0 1 2 3 4 5
         (48, 52), (55, 72), (66, 41), (73, 67), (76, 52), (79, 60), (83, 40), (85, 45),   # W X Y X, then lower highs
         (90, 26), (92, 33), (94, 30), (97, 44)]                                           # Z, then the break
DAILY_N = 124                                   # x axis runs to index 124: room on the right for the projection
DAILY_LABELS = [(7, 26, "1", "hi"), (11, 19, "2", "lo"), (26, 62, "3", "hi"), (31, 53, "4", "lo"), (40, 86, "5", "hi"),
                (48, 52, "W", "lo"), (55, 72, "X", "hi"), (66, 41, "Y", "lo"), (73, 67, "X", "hi"), (90, 26, "Z", "lo")]
TL = ((73, 67), (79, 60))             # trend line across the falling highs
CH_TOP = ((55, 72), (73, 67))         # channel top through the two X highs
CH_BOT_AT = (90, 26)                  # channel bottom: parallel, through Z
PULL = (101, 37.5)                    # projected pullback that holds above the line
TGT_I = 108                           # projection meets the channel top here (target 1)
NEXT = (120, 80)                      # next leg up
FAIL = (106, 24)                      # projected failure: back below the line

# ---- the 4H zoom: A B C (= W), X, then A B C with a triangle as B (= Y), then the break
H4 = [(0, 90), (10, 64), (16, 74.5), (28, 47), (35, 60.5),
      (42, 37), (45, 47), (48, 39), (51, 45.3), (54, 40.5), (57, 43.6), (59, 41.5),
      (68, 22), (71, 30), (73, 27), (77, 41)]
H4_LABELS = [(10, 64, "A", "lo"), (16, 74.5, "B", "hi"), (28, 47, "C", "lo"), (35, 60.5, "X", "hi"),
             (42, 37, "A", "lo"), (59, 41.5, "B", "hi"), (68, 22, "C", "lo")]
H4_TL = ((16, 74.5), (35, 60.5))
TRI = [(45, 47), (48, 39), (51, 45.3), (54, 40.5), (57, 43.6), (59, 41.5)]
