"""OTM CRT series, part 5/5: "The CRT checklist". English (otm-crt-ep5) and Thai (otm-crt-ep5-th) are built from this
same file; only LANG differs. Five boxes before every CRT trade: a higher-timeframe candle sets the range, price sweeps
one side, a candle closes back inside, the lower timeframe shifts with the entry at the middle of the fair value gap,
stop beyond the wick and target the other side. Miss one box and there's no trade. Save it, and tell me which pair you
use. Writes ../index.html, work/cues.json and work/timing.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otm import *

LANG = "th"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = "otm-crt-ep5" + ("-th" if LANG == "th" else "")
TOTAL = init(ROOT, LANG, COMP, "mix_crt5" + ("_th" if LANG == "th" else ""))
def KW(key, n): return W(G["marks"][key] + n)

ROWS = [("c1", None, ("HIGHER-TIMEFRAME CANDLE", "แท่งไทม์เฟรมใหญ่"), ("SETS THE RANGE", "กำหนดกรอบ")),
        ("c2", None, ("PRICE SWEEPS ONE SIDE", "ราคากวาดไปฝั่งหนึ่ง"), ("THE STOPS GET TAKEN", "สต็อปโดนเก็บ")),
        ("c3", None, ("CLOSE BACK INSIDE", "ปิดกลับเข้ากรอบ"), ("NO CLOSE, NO CRT", "ไม่ปิดกลับ = ไม่ใช่ CRT")),
        ("c4", "c4b", ("LOWER TIMEFRAME SHIFTS", "ไทม์เฟรมเล็กเปลี่ยนโครงสร้าง"), ("ENTRY: MIDDLE OF THE FAIR VALUE GAP", "เข้าที่กึ่งกลางแฟร์แวลูแก็ป")),
        ("c5", "c5b", ("STOP BEYOND THE WICK", "สต็อปเลยไส้เทียน"), ("TARGET: THE OTHER SIDE OF THE RANGE", "เป้าหมาย: อีกฝั่งของกรอบ"))]
Y0, DY = 600, 140
MISS = 2                                               # the row that goes missing in the "miss one box" beat

# 1  the checklist (frame 0 is the thumbnail: the title and the five boxes)
o1, c1 = 0, K("save") - 0.1
s = S(o1, c1, first=True)
sym_pill(s)
s.label(540, 330, L("BEFORE EVERY CRT TRADE", "ก่อนเข้าเทรด CRT ทุกครั้ง"), 40, WHITE, 1, 800, 0.04)
s.label(540, 430, L("THE CRT CHECKLIST", "เช็กลิสต์ CRT"), 64, GOLD, 1, 800, 0.04)
row_ids = []
for k, (key, subkey, main, sub) in enumerate(ROWS):
    yy = Y0 + DY * k
    box = s.raw(f'<rect id="@ID@" x="96" y="{yy - 34}" width="64" height="64" rx="12" fill="none" stroke="#ffffff" stroke-opacity="0.5" stroke-width="4"/>', "cb")
    num = s.label(128, yy + 12, str(k + 1), 34, GREY, 1, 800, 0)
    m = s.label(196, yy - 2, L(*main), 36, WHITE, 0.4, 800, 0.03, "start")
    sb = s.label(196, yy + 40, L(*sub), 24, LBL, 0.3, 700, 0.06, "start")
    ck = check(s, 128, yy - 2, 22, GREEN, 7)
    t = K(key)
    tl(f'tl.to("#{box}", {{attr: {{stroke: "{GREEN}", "stroke-opacity": 1}}, duration: 0.25}}, {t:.3f});')
    s.draw(ck, t + 0.05, 0.3); out(num, t, 0.15)
    s.fade(m, t, 0.3, to=1, frm=0.4); s.fade(sb, K(subkey) if subkey else t + 0.5, 0.3, to=1, frm=0.3)
    cue(t, ["tick-crisp_1", "tick-crisp_2", "tick-crisp_3", "tick-crisp_1", "tick-crisp_2"][k], -16)
    row_ids.append((box, m, sb, ck))
# miss one box, and there's no trade
box, m, sb, ck = row_ids[MISS]
out(ck, K("miss"), 0.2)
tl(f'tl.to("#{box}", {{attr: {{stroke: "{RED}"}}, duration: 0.2}}, {K("miss"):.3f});')
xm = xmark(s, 128, Y0 + DY * MISS - 2, 18, RED, 7); s.draw(xm, K("miss") + 0.15, 0.25)
for i in (m, sb): out(i, K("miss") + 0.1, 0.3, 0.35)
stamp = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="300" y="{Y0 + DY * 2 - 70}" width="480" height="120" rx="18" fill="none" stroke="{RED}" stroke-width="8"/>'
              f'<text x="540" y="{Y0 + DY * 2 + 14}" text-anchor="middle" font-family="{"Kanit" if TH() else "Montserrat"}" font-weight="800" font-size="{64 if TH() else 60}" '
              f'letter-spacing="{0 if TH() else 0.06}em" fill="{RED}">{L("NO TRADE", "ไม่มีเทรด")}</text></g>', "st")
tl(f'tl.fromTo("#{stamp}", {{opacity: 0, scale: 1.6, rotation: -8, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, rotation: -8, duration: 0.35, ease: "power3.in", immediateRender: false}}, {KW("miss", L(5, 1)):.3f});')
cue(KW("miss", L(5, 1)) + 0.3, "land_1", -16)
captions(s, [(K("c1") - 0.1, L("RUN IT BEFORE EVERY TRADE", "ไล่เช็กก่อนเทรดทุกครั้ง"), WHITE),
             (K("miss") - 0.1, L("MISS ONE BOX = NO TRADE", "ขาดข้อไหน = ไม่มีเทรด"), RED)], c1, 1450)

# 2  save this; check it before you click buy or sell
o2, c2 = K("save") - 0.1, K("ask") - 0.1
s = S(o2, c2)
series_tag(s, 5)
bm = s.raw(f'<path id="@ID@" d="M 470 640 H 610 V 860 L 540 805 L 470 860 Z" fill="{GOLD}" style="opacity:0;filter:drop-shadow(0 0 20px rgba(232,194,106,0.6))"/>', "bm")
s.pop(bm, K("save") + 0.1, 0.45, 0.4); cue(K("save") + 0.1, "bell_A4", -16)
sv = s.label(540, 960, L("SAVE THIS", "เซฟไว้"), 72, WHITE, 0, 800, 0.06); s.pop(sv, K("save") + 0.2, 0.4, 0.6)
ckb = s.label(540, 1060, L("CHECK IT BEFORE YOU CLICK", "เช็กก่อนกดทุกครั้ง"), 30, LBL, 0, 700, 0.1); s.fade(ckb, KW("save", L(3, 1)))
bb = s.pill(400, 1180, L("BUY", "ซื้อ"), UP, WHITE, 34); s.pop(bb, KW("save", 8) if not TH() else KW("save", 1) + 0.6, 0.35, 0.5)
ss = s.pill(680, 1180, L("SELL", "ขาย"), WHITE, "#0b0b0b", 34); s.pop(ss, (KW("save", 10) if not TH() else KW("save", 1) + 0.9), 0.35, 0.5)
cue(KW("save", 8) if not TH() else KW("save", 1) + 0.6, "click_1", -18)

# 3  which pair do you use? tell me in the comments
o3, c3 = K("ask") - 0.1, K("order") - 0.05
s = S(o3, c3)
series_tag(s, 5)
q = s.label(540, 600, L("WHICH PAIR DO YOU USE?", "คุณใช้คู่ไหน?"), 50, WHITE, 0, 800, 0.04); s.pop(q, K("ask"), 0.4, 0.6)
for k, (yc, left, right, key) in enumerate([(800, "4H", "5M", "ask"), (1020, L("DAILY", "รายวัน"), "1H", "ask2")]):
    t = K(key) + (L(1.0, 0.6) if k == 0 else 0.3)
    card = s.raw(f'<rect id="@ID@" x="170" y="{yc - 85}" width="740" height="170" rx="28" fill="#ffffff" fill-opacity="0.05" stroke="{GOLD}" stroke-width="3" style="opacity:0"/>', "cd")
    a = s.label(430, yc + 20, left, 56, WHITE, 0, 800, 0.04, "end")
    ar = s.path(f"M 470 {yc} L 590 {yc} M 566 {yc - 20} L 590 {yc} L 566 {yc + 20}", GOLD, 6, drawn=True, style="opacity:0")
    b = s.label(650, yc + 20, right, 56, GOLD, 0, 800, 0.04, "start")
    for i in (card, a, ar, b): s.pop(i, t, 0.35, 0.7)
    cue(t, "pop_" + str(k + 1), -18)
    if k == 0:
        orl = s.label(540, 935, L("OR", "หรือ"), 30, GREY, 0, 800, 0.2); s.fade(orl, K("ask2"))
bub = s.raw(f'<g id="@ID@" style="opacity:0"><rect x="380" y="1180" width="320" height="130" rx="30" fill="#11151b" stroke="#fff" stroke-width="3"/>'
            f'<path d="M 470 1308 L 450 1352 L 512 1308" fill="#11151b" stroke="#fff" stroke-width="3" stroke-linejoin="round"/>'
            + "".join(f'<circle cx="{490 + j * 50}" cy="1245" r="11" fill="{GOLD}"/>' for j in range(3)) + "</g>", "bb")
s.pop(bub, K("cm"), 0.4, 0.5); cue(K("cm"), "click-confirm_1", -18)
cm = s.label(540, 1430, L("TELL ME IN THE COMMENTS", "บอกกันในคอมเมนต์"), 34, WHITE, 0, 800, 0.08); s.fade(cm, K("cm") + 0.1, 0.35, y=10)

outro(K("order") - 0.05)
write()
