"""Synthetic example chart for "The Order Block" (not real market data).
A seeded decline (candles 0-18), the order block (candle 19: the last down candle), a strong push up that leaves a gap
(20-23), a drift, the pullback into the block (24-36, whose wick tags the middle of the block's body), the bounce (37)
and the rally (38-47).

Coordinates: price 0-100 maps to y BOT..TOP, candle index 0..NX maps to x X0..X1.
Candle colours: up #2962ff, down white."""
import random

X0, X1, TOP, BOT = 80, 1000, 600, 1240
UP, DOWN = "#2962ff", "#ffffff"
NX = 52

OB = 19                                   # the order block candle
OB_O, OB_C, OB_H, OB_L = 36, 30, 37, 28
OB_MID = (OB_O + OB_C) / 2                # 33: the buy limit
STOP = 26.6                               # just under the block's low
FILL = 36                                 # the pullback candle whose wick tags the buy limit
GAP_LO, GAP_HI = OB_H, 44.5               # gap between the block's high and candle 21's low


def _decline(seed=11):
    """candles 0..18 along pivots, ending with a close at the block's open"""
    pv = [(0, 58), (3, 68), (7, 52), (10, 60), (14, 41), (16, 46.5), (18, OB_O)]
    path = []
    for (i0, p0), (i1, p1) in zip(pv, pv[1:]):
        path += [p0 + (p1 - p0) * (i - i0) / (i1 - i0) for i in range(i0, i1)]
    path.append(pv[-1][1])
    r = random.Random(seed)
    out, prev = [], path[0] - 2
    for i, p in enumerate(path):
        c = p + (r.uniform(-1.4, 1.4) if 0 < i < 18 else 0)
        o = prev
        h = max(o, c) + r.uniform(0.4, 1.5)
        lo = min(o, c) - r.uniform(0.4, 1.5)
        if i >= 16: lo = max(lo, OB_C + 2.5)         # the block stays the low of the move
        out.append((o, h, lo, c))
        prev = c
    return out


# (open, high, low, close)
CANDLES = _decline() + [
    (OB_O, OB_H, OB_L, OB_C),                                            # 19 the order block
    (30, 46, 29.6, 45), (45, 57, GAP_HI, 55), (55, 64.5, 53.5, 63), (63, 68, 61.5, 66),   # 20-23 the push
    (66, 67.5, 62, 64), (64, 69, 63, 67), (67, 68, 63.5, 65), (65, 66, 60.5, 62),         # 24-27 drift
    (62, 65, 60, 63.5), (63.5, 64, 57, 58), (58, 59, 51, 52), (52, 55.5, 50.5, 54),       # 28-31
    (54, 54.5, 46, 47), (47, 48, 40, 41), (41, 44, 39, 43), (43, 43.5, 35.5, 36.5),       # 32-35 the pullback
    (36.5, 37.5, 32.4, 34.5),                                            # 36 tags the middle of the body
    (34.5, 42, 33.8, 41),                                                # 37 the bounce
    (41, 49, 40, 48), (48, 49.5, 44.5, 46), (46, 55, 45.5, 54), (54, 61, 53, 60),         # 38-41 the rally
    (60, 62, 57, 58), (58, 67, 57.5, 66), (66, 72.5, 65, 71), (71, 72, 67.5, 69),
    (69, 77, 68.5, 76), (76, 82, 75, 80)]                                # 42-47


class Chart:
    def __init__(self, c=CANDLES, nx=NX, top=TOP, bot=BOT, x0=X0, x1=X1):
        self.c, self.nx, self.top, self.bot, self.x0, self.x1 = c, nx, top, bot, x0, x1

    def x(self, i): return self.x0 + (self.x1 - self.x0) * i / self.nx
    def y(self, p): return self.bot - (self.bot - self.top) * p / 100
    def xy(self, i, p): return (round(self.x(i), 1), round(self.y(p), 1))
    @property
    def sp(self): return (self.x1 - self.x0) / self.nx
    @property
    def bw(self): return self.sp * 0.7

    def candle(self, i, up=UP, down=DOWN, extra=""):
        o, h, lo, c = self.c[i]
        col = up if c >= o else down
        x = self.x(i)
        yt, yb = self.y(max(o, c)), self.y(min(o, c))
        return (f'<g {extra}><line x1="{x:.1f}" y1="{self.y(h):.1f}" x2="{x:.1f}" y2="{self.y(lo):.1f}" stroke="{col}" stroke-width="2"/>'
                f'<rect x="{x - self.bw / 2:.1f}" y="{yt:.1f}" width="{self.bw:.1f}" height="{max(2, yb - yt):.1f}" fill="{col}"/></g>')

    def candles(self, i0=0, i1=None):
        i1 = len(self.c) if i1 is None else i1
        return [self.candle(i) for i in range(i0, i1)]


if __name__ == "__main__":
    for i, (o, h, lo, c) in enumerate(CANDLES):
        assert lo <= min(o, c) and h >= max(o, c), (i, o, h, lo, c)
    assert all(CANDLES[i][3] >= CANDLES[i][0] for i in range(20, 24)), "push is all up candles"
    assert CANDLES[OB][3] < CANDLES[OB][0], "the block is a down candle"
    assert CANDLES[FILL][2] < OB_MID < CANDLES[FILL][3] and CANDLES[FILL][2] > OB_L
    assert CANDLES[21][2] > OB_H, "gap"
    print("ok", len(CANDLES))
