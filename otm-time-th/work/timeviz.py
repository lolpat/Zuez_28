"""OTM "Not much time": an original general-motivation Reel (time is short; do one thing today; did I get better today?
this is it). OTM glowing style, phrase captions with the spoken word in gold (from mind.py), EN Quentin / TH Patinya.
Inspired by the idea of a motivational TikTok the trader shared; no words, footage or audio from it are used."""
from otm import *
from mind import kw, lbl, pill, phrase_captions

def anim(s, sel, frm, to, t, d, ease="none"):
    tl(f'tl.fromTo("#{sel}", {frm}, {{...{to}, duration: {d:.3f}, ease: "{ease}", immediateRender: false}}, {t:.3f});')

def scenes():
    # 1  the hourglass
    o, c = 0, K("count") - 0.1
    s = S(o, c, first=True)
    s.spot(540, 0.5, "232,194,106", 40, 240, 1180)
    s.path("M 400 600 L 680 600 L 680 622 Q 680 765 560 870 Q 680 975 680 1118 L 680 1140 L 400 1140 L 400 1118 Q 400 975 520 870 "
           "Q 400 765 400 622 Z", WHITE, 5, drawn=True, style="filter:drop-shadow(0 0 12px rgba(255,255,255,0.35))")
    top = s.raw(f'<path id="@ID@" d="M 425 690 L 655 690 Q 645 790 540 862 Q 435 790 425 690 Z" fill="{GOLD}" fill-opacity="0.85"/>', "sd")
    anim(s, top, '{scaleY: 1, transformOrigin: "50% 100%"}', '{scaleY: 0.25}', 0, c)
    bot = s.raw(f'<path id="@ID@" d="M 418 1136 Q 540 1010 662 1136 Z" fill="{GOLD}" fill-opacity="0.85"/>', "sd")
    anim(s, bot, '{scaleY: 0.2, transformOrigin: "50% 100%"}', '{scaleY: 1}', 0, c)
    st = s.raw(f'<line id="@ID@" x1="540" y1="868" x2="540" y2="1120" stroke="{GOLD}" stroke-width="4" stroke-dasharray="8 10"/>', "sm")
    anim(s, st, '{strokeDashoffset: 0}', '{strokeDashoffset: -180}', 0, c)
    tm = lbl(s, 540, 520, "TIME", "เวลา", 40, GOLD, 0, 800, 0.3); s.fade(tm, 0.3, 0.4)

    # 2  about 4,000 weeks; some are already gone
    o, c = K("count") - 0.1, K("later") - 0.1
    s = S(o, c)
    pid, pid2 = s.uid("pt"), s.uid("pt")
    s.raw(f'<defs><pattern id="{pid}" width="11.1" height="11.1" patternUnits="userSpaceOnUse"><circle cx="5.5" cy="5.5" r="2.3" fill="#ffffff" fill-opacity="0.75"/></pattern>'
          f'<pattern id="{pid2}" width="11.1" height="11.1" patternUnits="userSpaceOnUse"><circle cx="5.5" cy="5.5" r="2.6" fill="{RED}" fill-opacity="0.9"/></pattern></defs>'
          '<rect id="@ID@" x="0" y="0" width="0" height="0"/>', "df")
    gr = s.raw(f'<rect id="@ID@" x="140" y="560" width="799" height="622" fill="url(#{pid})"/>', "gr")
    tl(f'tl.set("#{gr}", {{scaleY: 0, transformOrigin: "50% 0%"}}, {o:.3f});')
    anim(s, gr, '{scaleY: 0, transformOrigin: "50% 0%"}', '{scaleY: 1}', K("weeks"), 1.4, "power2.out")
    wl = lbl(s, 540, 500, "ABOUT 4,000 WEEKS", "ประมาณ 4,000 สัปดาห์", 40, WHITE, 0, 800, 0.1); s.fade(wl, kw("weeks", 2, 0), 0.35)
    lk = lbl(s, 540, 1240, "IF YOU'RE LUCKY", "ถ้าโชคดี", 26, GREY, 0, 700, 0.2); s.fade(lk, K("all") + 0.1, 0.3)
    gn = s.raw(f'<rect id="@ID@" x="140" y="560" width="799" height="244" fill="url(#{pid2})"/>', "gn")
    tl(f'tl.set("#{gn}", {{scaleY: 0, transformOrigin: "50% 0%"}}, {o:.3f});')
    anim(s, gn, '{scaleY: 0, transformOrigin: "50% 0%"}', '{scaleY: 1}', K("gone") + 0.2, 1.3, "power1.inOut")
    gl = pill(s, 540, 682, "ALREADY GONE", "ผ่านไปแล้ว", RED, "#fff", 32); s.pop(gl, kw("gone", 5, 1) + 0.1, 0.4, 0.5); cue(kw("gone", 5, 1) + 0.1, "swell_1", -24)

    # 3  someday, later, next year: dreams fade
    o, c = K("later") - 0.1, K("not") - 0.1
    s = S(o, c)
    for k, (en, th) in enumerate([("SOMEDAY", "สักวัน"), ("LATER", "ไว้ก่อน"), ("NEXT YEAR", "ปีหน้า")]):
        p = s.pill(540, 640 + 110 * k, L(en, th), "#1b1e23", LBL, 32, 0, glow=False)
        s.fade(p, kw("later", k if k < 2 else 2, k) + 0.05, 0.3, y=14)
    star = "M 540 940 L 563 1003 L 630 1005 L 577 1046 L 596 1110 L 540 1072 L 484 1110 L 503 1046 L 450 1005 L 517 1003 Z"
    sr = s.raw(f'<path id="@ID@" d="{star}" fill="{GOLD}" style="filter:drop-shadow(0 0 22px rgba(232,194,106,0.8))"/>', "st")
    s.pop(sr, K("later") + 0.3, 0.5, 0.5)
    tl(f'tl.to("#{sr}", {{opacity: 0.12, y: 40, duration: 1.6, ease: "power1.in"}}, {kw("lie", 4, 1):.3f});')
    dl = lbl(s, 540, 1200, "DREAMS DIE QUIETLY", "ความฝันตายไปเงียบๆ", 28, GREY, 0, 700, 0.16); s.fade(dl, kw("lie", 4, 1) + 0.3, 0.5)

    # 4  not quit everything: one thing today, for future you
    o, c = K("not") - 0.1, K("ask") - 0.1
    s = S(o, c)
    q = lbl(s, 540, 620, "QUIT EVERYTHING", "ทิ้งทุกอย่าง", 40, GREY, 0, 800, 0.1); s.fade(q, K("not") + 0.2, 0.3)
    xq = s.path("M 330 607 L 750 607", RED, 6); s.draw(xq, kw("not", 3, 0) + 0.3, 0.4)
    one = s.label(360, 1020, "1", 260, GOLD, 0, 800, 0); s.pop(one, kw("one", 3, 0) + 0.1, 0.45, 0.4)
    ol = lbl(s, 360, 1090, "THING TODAY", "อย่าง วันนี้", 26, GOLD, 0, 800, 0.2); s.fade(ol, kw("one", 5, 0) + 0.1, 0.3)
    cue(kw("one", 3, 0) + 0.1, "bell_C5", -22)
    ar = arrow(s, 480, 930, 660, 930, GOLD, 6, 24); show_arrow(s, ar, K("future") + 0.1, 0.4)
    ck = check(s, 810, 880, 40, GOLD, 9); s.draw(ck, kw("future", 4, 1), 0.35)
    fl = lbl(s, 810, 990, "FUTURE YOU", "ตัวเราในอนาคต", 30, WHITE, 0, 800, 0.12); s.fade(fl, kw("future", 2, 0) + 0.1, 0.3)
    cue(kw("future", 4, 1), "bell_G4", -22)

    # 5  every night: did I get better today?
    o, c = K("ask") - 0.1, K("yes") - 0.1
    s = S(o, c)
    mn = s.raw('<g id="@ID@" style="opacity:0;filter:drop-shadow(0 0 18px rgba(255,255,255,0.45))"><circle cx="540" cy="680" r="80" fill="#ffffff"/>'
               '<circle cx="575" cy="655" r="74" fill="#000000"/></g>', "mn")
    s.fade(mn, K("ask") + 0.15, 0.5)
    en_ = lbl(s, 540, 820, "EVERY NIGHT", "ทุกคืน", 26, GREY, 0, 700, 0.3); s.fade(en_, K("ask") + 0.3, 0.3)
    qb = lbl(s, 540, 920, "DID I GET BETTER TODAY?", "วันนี้ เราเก่งขึ้นไหม?", 44, GOLD, 0, 800, 0.04); s.pop(qb, K("better") + 0.1, 0.45, 0.6)
    steps = s.path("M 380 1200 L 460 1200 L 460 1160 L 540 1160 L 540 1120 L 620 1120", WHITE, 5); s.draw(steps, K("better") + 0.3, 0.6)
    last = s.path("M 620 1120 L 620 1080 L 700 1080", GOLD, 7); s.draw(last, kw("better", 5, 1), 0.35)
    pl = lbl(s, 740, 1060, "+1%", "+1%", 34, GOLD, 0, 800, 0.04); s.pop(pl, kw("better", 5, 1) + 0.2, 0.35, 0.5)
    cue(kw("better", 5, 1) + 0.2, "bell_A4", -20)

    # 6  yes: building / no: the day is gone, never comes back
    o, c = K("yes") - 0.1, K("now") - 0.1
    s = S(o, c)
    for k in range(4):
        b = s.raw(f'<rect id="@ID@" x="{230 + (k % 2) * 20}" y="{1030 - 80 * k}" width="200" height="66" rx="8" fill="{GOLD}" '
                  f'style="opacity:0;filter:drop-shadow(0 0 10px rgba(232,194,106,0.5))"/>', "bk")
        s.pop(b, K("yes") + 0.2 + 0.18 * k, 0.3, 0.6)
    bl = lbl(s, 340, 1160, "BUILDING", "กำลังสร้าง", 30, GOLD, 0, 800, 0.16); s.fade(bl, kw("yes", 3, 1), 0.3)
    cue(K("yes") + 0.2, "bell_C5", -24)
    dt = s.raw('<g id="@ID@" style="opacity:0"><rect x="630" y="760" width="220" height="250" rx="18" fill="none" stroke="#ffffff" stroke-width="4"/>'
               '<rect x="630" y="760" width="220" height="56" rx="18" fill="#ffffff"/>'
               f'<text x="740" y="800" text-anchor="middle" font-family="{"Kanit" if TH() else "Montserrat"}" font-weight="800" font-size="26" fill="#0b0b0b">{L("TODAY", "วันนี้")}</text>'
               '<circle cx="740" cy="910" r="34" fill="none" stroke="#7d838c" stroke-width="4"/></g>', "dt")
    s.fade(dt, K("no") + 0.05, 0.3)
    tl(f'tl.to("#{dt}", {{opacity: 0, y: 120, rotation: 12, transformOrigin: "50% 50%", duration: 1.2, ease: "power2.in"}}, {kw("no", 4, 1):.3f});')
    xg = xmark(s, 740, 900, 40, RED, 8); s.draw(xg, kw("no", 4, 1) + 0.9, 0.3)
    gl = lbl(s, 740, 1160, "GONE", "หายไป", 30, RED, 0, 800, 0.16); s.fade(gl, kw("no", 4, 1) + 0.9, 0.3)
    nb = lbl(s, 540, 1270, "IT NEVER COMES BACK", "มันไม่มีวันกลับมา", 28, LBL, 0, 700, 0.14); s.fade(nb, K("back") + 0.2, 0.4)
    cue(kw("no", 4, 1), "whoosh-short_2", -26)

    # 7  stop waiting for the perfect moment: NOW
    o, c = K("now") - 0.1, K("order") - 0.05
    s = S(o, c)
    pm = lbl(s, 540, 560, "THE PERFECT MOMENT", "จังหวะที่สมบูรณ์แบบ", 34, GREY, 0, 800, 0.1); s.fade(pm, K("now") + 0.2, 0.3)
    xp = s.path("M 290 548 L 790 548", RED, 6); s.draw(xp, kw("now", 1, 0) + 0.3, 0.4)
    s.raw('<circle id="@ID@" cx="540" cy="880" r="210" fill="none" stroke="#ffffff" stroke-width="5" style="filter:drop-shadow(0 0 14px rgba(255,255,255,0.3))"/>', "ck")
    ticks = "".join(f'<line x1="{540 + 185 * math.cos(math.radians(a)):.1f}" y1="{880 + 185 * math.sin(math.radians(a)):.1f}" '
                    f'x2="{540 + 200 * math.cos(math.radians(a)):.1f}" y2="{880 + 200 * math.sin(math.radians(a)):.1f}" stroke="#7d838c" stroke-width="4"/>' for a in range(0, 360, 30))
    s.raw(f'<g id="@ID@">{ticks}</g>', "tk")
    hd = s.raw(f'<line id="@ID@" x1="540" y1="880" x2="540" y2="720" stroke="{GOLD}" stroke-width="7" stroke-linecap="round"/>', "hd")
    tl(f'tl.fromTo("#{hd}", {{rotation: -60, svgOrigin: "540 880"}}, {{rotation: 300, duration: {K("this") - o:.3f}, ease: "power1.inOut", immediateRender: false}}, {o:.3f});')
    s.raw('<circle id="@ID@" cx="540" cy="880" r="10" fill="#e8c26a"/>', "cd")
    s.spot(540, 0, "232,194,106", 40, 260, 1240)
    nw = s.label(540, 1240, L("NOW", "ตอนนี้"), 120, GOLD, 0, 800, 0.08); s.pop(nw, K("this") + 0.15, 0.5, 0.5)
    cue(K("this") + 0.15, "bell_A4", -16)

def build():
    scenes(); phrase_captions()
    outro(K("order") - 0.05)
    write()
