"""Builds the OTM CRT film: cuts each slide into animated layers, writes the scene compositions and index.html,
and writes the sound cue list (work/cues.json) that mix.py turns into assets/audio/sfx.wav.

Run from anywhere: python3 work/gen.py  (paths are relative to this file's project root)
"""
import json, math, os
import numpy as np
import cv2
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1920
BLUE = "#1f5cff"

# --- the film ---------------------------------------------------------------------------------------------------
# layer: (name, kind, rects, start)   kinds: slam wipe wipeslow grow stamp rise pop
# rects are (x0, y0, x1, y1) in 1080x1920; a later layer owns the pixels it shares with an earlier one.
SCENES = [
    dict(id="s1", slide="s1_cover", dur=4.6, enter="none", exit="dive", dive=(595, 655),
         layers=[("title", "slam", [(50, 110, 960, 405)], 0.0),
                 ("sub", "wipe", [(200, 405, 880, 478)], 0.35),
                 ("key", "wipe", [(420, 500, 820, 548)], 0.55),
                 ("chart", "wipeslow", [(0, 548, 1080, 1640)], 0.6),
                 ("crt3", "stamp", [(470, 555, 900, 945)], 1.1),
                 ("char", "rise", [(330, 945, 930, 1755), (520, 860, 600, 945)], 1.35)],
         sparks=["crt3"], highlight=None),
    dict(id="s2", slide="s2_what", dur=5.8, enter="zoom", exit="glitch", dive=(615, 790),
         layers=[("title", "slam", [(55, 180, 1065, 425)], 0.15),
                 ("char", "rise", [(0, 1075, 430, 1665), (430, 1300, 670, 1665)], 0.45),
                 ("l1", "wipe", [(40, 440, 1040, 505)], 0.6),
                 ("l2", "wipe", [(40, 505, 1040, 562)], 0.75),
                 ("l3", "wipe", [(40, 562, 1040, 628)], 0.9),
                 ("c1", "grow", [(420, 720, 560, 1305)], 1.3),
                 ("c2", "grow", [(555, 640, 675, 945)], 1.55),
                 ("c3", "grow", [(675, 770, 805, 1435)], 1.8),
                 ("crth", "wipe", [(470, 715, 1040, 760)], 2.15),
                 ("crtl", "wipe", [(470, 1280, 1040, 1325)], 2.35)],
         sparks=[], highlight=dict(kind="ellipse", cx=615, cy=700, rx=78, ry=100, t=2.75, color="#ff2d3d")),
    dict(id="s3", slide="s3_valid", dur=5.8, enter="zoom", exit="whipL", dive=(750, 790),
         layers=[("title", "slam", [(35, 170, 1060, 405)], 0.15),
                 ("char", "rise", [(170, 1180, 1020, 1738)], 0.45),
                 ("t1", "wipe", [(90, 408, 975, 462)], 0.6),
                 ("t2", "wipe", [(90, 462, 975, 514)], 0.75),
                 ("dl", "grow", [(70, 612, 520, 1212)], 1.1),
                 ("dr", "grow", [(520, 535, 1045, 1212)], 1.45),
                 ("x", "stamp", [(338, 935, 460, 1060)], 2.0),
                 ("ok", "stamp", [(845, 920, 995, 1065)], 2.45)],
         sparks=["x", "ok"], highlight=None),
    dict(id="s4", slide="s4_power3", dur=6.2, enter="whipL", exit="dive", dive=(550, 900),
         layers=[("title", "slam", [(35, 195, 1065, 410)], 0.15),
                 ("char", "rise", [(0, 1150, 560, 1700)], 0.45),
                 ("t1", "wipe", [(70, 438, 1015, 500)], 0.6),
                 ("p3", "stamp", [(260, 498, 830, 598)], 0.95),
                 ("st1", "grow", [(80, 705, 495, 1150), (365, 1150, 495, 1315)], 1.5),
                 ("st2", "grow", [(495, 625, 955, 998)], 2.0),
                 ("st3", "grow", [(612, 858, 1055, 1415)], 2.5)],
         sparks=["p3"], highlight=None),
    dict(id="s5", slide="s5_theory", dur=6.2, enter="zoom", exit="glitch", dive=(450, 1270),
         layers=[("title", "slam", [(35, 180, 1065, 412)], 0.15),
                 ("char", "rise", [(630, 1120, 1080, 1700)], 0.45),
                 ("b1", "wipe", [(50, 415, 1075, 546)], 0.6),
                 ("b2", "wipe", [(50, 546, 1075, 616)], 0.85),
                 ("b3", "wipe", [(50, 616, 1075, 750)], 1.1),
                 ("b4", "wipe", [(50, 750, 1075, 892)], 1.35),
                 ("diag", "grow", [(160, 915, 750, 1635)], 1.75)],
         sparks=[], highlight=dict(kind="underline", x0=500, x1=885, y=822, t=2.4, color=BLUE)),
    dict(id="s6", slide="s6_time", dur=6.2, enter="zoom", exit="whipU", dive=(500, 1295),
         layers=[("title", "slam", [(35, 180, 1045, 410)], 0.15),
                 ("char", "rise", [(585, 1125, 1080, 1700)], 0.45),
                 ("sub", "wipe", [(90, 412, 990, 498)], 0.6),
                 ("fx", "stamp", [(50, 525, 390, 608)], 0.9),
                 ("fxl", "wipe", [(100, 605, 945, 728)], 1.1),
                 ("ix", "stamp", [(50, 770, 1025, 858)], 1.45),
                 ("ixl", "wipe", [(100, 855, 965, 922)], 1.65),
                 ("note", "wipe", [(50, 960, 1030, 1098)], 1.9),
                 ("ic1", "pop", [(85, 1165, 355, 1425)], 2.3),
                 ("ic2", "pop", [(365, 1165, 600, 1425)], 2.55)],
         sparks=["fx", "ix"], highlight=None),
    dict(id="s7", slide="s7_turtle", dur=6.2, enter="whipU", exit="dive", dive=(500, 540),
         layers=[("title", "slam", [(80, 180, 1065, 410)], 0.15),
                 ("char", "rise", [(605, 1135, 1080, 1700)], 0.45),
                 ("diag", "grow", [(290, 405, 905, 1188)], 0.8),
                 ("sweep", "stamp", [(392, 492, 612, 592)], 1.45),
                 ("b1", "wipe", [(50, 1186, 615, 1248)], 1.85),
                 ("b2", "wipe", [(50, 1248, 615, 1308)], 2.0),
                 ("b3", "wipe", [(50, 1308, 615, 1368)], 2.15),
                 ("b4", "wipe", [(50, 1368, 615, 1486)], 2.3),
                 ("b5", "wipe", [(50, 1486, 645, 1552)], 2.45)],
         sparks=["sweep"], highlight=None),
    dict(id="s8", slide="s8_tf", dur=6.6, enter="zoom", exit="dive", dive=(360, 1490),
         layers=[("title", "slam", [(50, 155, 1065, 378)], 0.15),
                 ("char", "rise", [(540, 1185, 1080, 1698)], 0.45),
                 ("th", "wipe", [(125, 382, 955, 474)], 0.6),
                 ("r1", "wipe", [(125, 474, 955, 549)], 0.8),
                 ("r2", "wipe", [(125, 549, 955, 624)], 0.95),
                 ("r3", "wipe", [(125, 624, 955, 702)], 1.1),
                 ("r4", "wipe", [(125, 702, 955, 779)], 1.25),
                 ("r5", "wipe", [(125, 779, 955, 855)], 1.4),
                 ("r6", "wipe", [(125, 855, 955, 935)], 1.55),
                 ("seq", "wipe", [(25, 955, 1075, 1028)], 1.85),
                 ("i1", "wipe", [(90, 1028, 600, 1082)], 2.05),
                 ("i2", "wipe", [(90, 1082, 600, 1130)], 2.15),
                 ("i3", "wipe", [(90, 1130, 600, 1178)], 2.25),
                 ("i4", "wipe", [(90, 1178, 600, 1226)], 2.35),
                 ("i5", "wipe", [(90, 1226, 600, 1275)], 2.45),
                 ("mini", "grow", [(120, 1275, 560, 1698)], 2.75)],
         sparks=[], highlight=dict(kind="box", x0=125, y0=474, x1=955, y1=549, t=3.1, color="#ff2d3d")),
]
END = dict(id="end", dur=4.0)

VO_DURS = f"{ROOT}/work/vo/durs.json"
if os.path.exists(VO_DURS):
    _d = json.load(open(VO_DURS))
    for sc in SCENES:
        vo = _d[sc["id"]]
        sc["vo_start"] = 0.15 if sc["id"] == "s1" else 0.35
        sc["dur"] = round(math.ceil((sc["vo_start"] + vo + 0.75) * 10) / 10, 1)
        # spread the build across the line: the last piece lands at about 65% of the voice
        late = [l[3] for l in sc["layers"] if l[3] > 0.45]
        if late:
            k = max(1.0, (sc["vo_start"] + 0.85 * vo - 0.45) / (max(late) - 0.45))
            sc["layers"] = [(n, kd, r, t if t <= 0.45 else round(0.45 + (t - 0.45) * k, 2)) for n, kd, r, t in sc["layers"]]
            if sc.get("highlight"):
                sc["highlight"]["t"] = round(min(0.45 + (sc["highlight"]["t"] - 0.45) * k, sc["dur"] - 1.6), 2)
    END["vo_start"] = 0.3
    END["dur"] = round(max(4.0, 0.3 + _d["end"] + 2.2), 1)

SPARK_COLOR = {"x": "#ff2d3d", "ok": "#22c55e", "sweep": "#ff6b8a", "fx": "#ff2d3d", "ix": "#ff2d3d"}

# --- cutting the slides ---------------------------------------------------------------------------------------------
def rect_mask(rects):
    m = np.zeros((H, W), bool)
    for x0, y0, x1, y1 in rects:
        m[max(0, y0):min(H, y1), max(0, x0):min(W, x1)] = True
    return m

def cut(scene):
    img = np.array(Image.open(f"{ROOT}/assets/slides/{scene['slide']}.jpg").convert("RGB"))
    layers = scene["layers"]
    owned_later = np.zeros((H, W), bool)
    out = {}
    for name, kind, rects, t in reversed(layers):           # later layers own shared pixels
        m = rect_mask(rects) & ~owned_later
        owned_later |= rect_mask(rects)
        ys, xs = np.where(m)
        x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
        rgba = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
        rgba[..., :3] = img[y0:y1, x0:x1]
        rgba[..., 3] = m[y0:y1, x0:x1] * 255
        Image.fromarray(rgba).save(f"{ROOT}/assets/layers/{scene['id']}_{name}.png", optimize=True)
        out[name] = (int(x0), int(y0), int(x1 - x0), int(y1 - y0))
    # the plate: the slide with every layer's area painted out (inpainted at half size, then pasted back)
    # the slides' content ground is a light grey paper: fill with its median colour plus a faint fixed grain
    light = img[(img.min(axis=2) > 225) & ~owned_later]
    base = np.median(light, axis=0) if len(light) else np.array([246, 247, 249])
    grain = np.random.default_rng(7).normal(0, 1.6, (H, W, 1))
    filled = np.clip(base[None, None, :] + grain, 0, 255).astype(np.uint8)
    soft = cv2.GaussianBlur(owned_later.astype(np.float32), (0, 0), 3)[..., None]
    plate = (img * (1 - soft) + filled * soft).astype(np.uint8)
    Image.fromarray(plate).save(f"{ROOT}/assets/plates/{scene['id']}.jpg", quality=92)
    return out

# --- scene html -----------------------------------------------------------------------------------------------------
SHAKE_X = [0.9, -0.75, 0.6, -0.8, 0.5, -0.45, 0.3, -0.2]
SHAKE_Y = [-0.5, 0.8, -0.6, 0.45, -0.7, 0.3, -0.25, 0.12]

def spark_vectors(n, seed):
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n + (seed * 0.37) % 0.5
        d = 120 + ((i * 53 + seed * 31) % 90)
        out.append((round(math.cos(a) * d), round(math.sin(a) * d), 8 + (i * 7 + seed) % 10))
    return out

def scene_html(sc, boxes, cues, t0):
    sid = sc["id"]; D = sc["dur"]
    dx, dy = sc["dive"]
    L = []    # markup
    J = []    # script lines
    css = []
    L.append(f'<img id="{sid}-plate" class="{sid}-full" src="assets/plates/{sid}.jpg" alt="" />')
    for i, (name, kind, rects, t) in enumerate(sc["layers"]):
        x, y, w, h = boxes[name]
        lid = f"{sid}-{name}"
        ov = "hidden" if kind == "rise" else "visible"
        L.append(f'<div id="{lid}" class="{sid}-lyr" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;overflow:{ov};z-index:{10 + i}">'
                 f'<img id="{lid}-img" src="assets/layers/{sid}_{name}.png" alt="" style="width:{w}px;height:{h}px" /></div>')
        if kind == "slam":
            J.append(f'tl.fromTo("#{lid}", {{opacity: {1 if t == 0 else 0}, scale: {1.35 if t == 0 else 1.75}, filter: "blur({4 if t == 0 else 14}px)"}}, '
                     f'{{opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.34, ease: "expo.out"}}, {t});')
            J.append(f'shake(tl, "#{sid}-shake", {t + 0.1:.2f}, 22);')
            J.append(f'tl.fromTo("#{sid}-pop", {{opacity: 0.75}}, {{opacity: 0, duration: 0.16, ease: "power2.out", immediateRender: false}}, {t + 0.08:.2f});')
            css.append(f'#{sid}-sweep {{ left:{x}px; top:{y}px; width:{w}px; height:{h}px; -webkit-mask-image:url(assets/layers/{sid}_{name}.png); mask-image:url(assets/layers/{sid}_{name}.png); -webkit-mask-size:100% 100%; mask-size:100% 100%; }}')
            J.append(f'tl.fromTo("#{sid}-sweep-bar", {{xPercent: -120}}, {{xPercent: 260, duration: 0.7, ease: "power2.inOut"}}, {t + 0.4:.2f});')
            cues.append(dict(t=t0 + t + 0.06, snd="hit", gain=-8))
        elif kind in ("wipe", "wipeslow"):
            dur = 0.95 if kind == "wipeslow" else 0.36
            J.append(f'tl.fromTo("#{lid}-img", {{clipPath: "inset(0% 100% 0% 0%)"}}, {{clipPath: "inset(0% 0% 0% 0%)", duration: {dur}, ease: "{"power2.inOut" if kind == "wipeslow" else "power3.out"}"}}, {t});')
            J.append(f'tl.fromTo("#{lid}", {{x: -26, opacity: 0}}, {{x: 0, opacity: 1, duration: {dur * 0.8:.2f}, ease: "expo.out"}}, {t});')
            cues.append(dict(t=t0 + t + 0.02, snd="swish" if kind == "wipeslow" else "tick", gain=-15 if kind == "wipeslow" else -20))
        elif kind == "grow":
            J.append(f'tl.fromTo("#{lid}-img", {{clipPath: "inset(100% 0% 0% 0%)"}}, {{clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "expo.out"}}, {t});')
            J.append(f'tl.fromTo("#{lid}", {{y: 40}}, {{y: 0, duration: 0.45, ease: "expo.out"}}, {t});')
            cues.append(dict(t=t0 + t + 0.03, snd="pop", gain=-14))
        elif kind == "stamp":
            J.append(f'tl.fromTo("#{lid}", {{opacity: 0, scale: 2.8, rotation: -8}}, {{opacity: 1, scale: 1, rotation: 0, duration: 0.3, ease: "back.out(2.2)"}}, {t});')
            J.append(f'shake(tl, "#{sid}-shake", {t + 0.2:.2f}, 14);')
            cues.append(dict(t=t0 + t + 0.2, snd="stamp", gain=-9))
        elif kind == "rise":
            J.append(f'tl.fromTo("#{lid}-img", {{y: {h + 10}}}, {{y: 0, duration: 0.62, ease: "back.out(1.25)"}}, {t});')
            cues.append(dict(t=t0 + t + 0.05, snd="rise", gain=-14))
        elif kind == "pop":
            J.append(f'tl.fromTo("#{lid}", {{opacity: 0, scale: 0.2, rotation: 10}}, {{opacity: 1, scale: 1, rotation: 0, duration: 0.42, ease: "back.out(1.9)"}}, {t});')
            cues.append(dict(t=t0 + t + 0.05, snd="pop", gain=-13))
    # sparks on stamps
    for k, name in enumerate(sc.get("sparks", [])):
        x, y, w, h = boxes[name]
        cx, cy = x + w / 2, y + h / 2
        t = next(l[3] for l in sc["layers"] if l[0] == name) + 0.2
        col = SPARK_COLOR.get(name, BLUE)
        for i, (vx, vy, s) in enumerate(spark_vectors(12, k + 3)):
            pid = f"{sid}-sp{k}-{i}"
            L.append(f'<div id="{pid}" class="{sid}-spark" style="left:{cx - s / 2:.0f}px;top:{cy - s / 2:.0f}px;width:{s}px;height:{s}px;background:{col}"></div>')
            J.append(f'tl.fromTo("#{pid}", {{x: 0, y: 0, opacity: 1, scale: 1}}, {{x: {vx * (1 + w / 600):.0f}, y: {vy * (1 + h / 600):.0f}, opacity: 0, scale: 0.3, duration: 0.5, ease: "power3.out", immediateRender: false}}, {t:.2f});')
    # hand-drawn highlight
    hl = sc.get("highlight")
    if hl:
        if hl["kind"] == "ellipse":
            path = f'<ellipse cx="{hl["cx"]}" cy="{hl["cy"]}" rx="{hl["rx"]}" ry="{hl["ry"]}" pathLength="1" />'
        elif hl["kind"] == "underline":
            path = f'<path d="M{hl["x0"]} {hl["y"]} Q {(hl["x0"] + hl["x1"]) / 2:.0f} {hl["y"] + 10} {hl["x1"]} {hl["y"] - 4}" pathLength="1" />'
        else:
            path = f'<rect x="{hl["x0"]}" y="{hl["y0"]}" width="{hl["x1"] - hl["x0"]}" height="{hl["y1"] - hl["y0"]}" rx="10" pathLength="1" />'
        L.append(f'<svg id="{sid}-hl" class="{sid}-full" viewBox="0 0 {W} {H}" style="z-index:60" fill="none" stroke="{hl["color"]}" stroke-width="9" stroke-linecap="round"><g id="{sid}-hl-g">{path}</g></svg>')
        J.append(f'tl.fromTo("#{sid}-hl-g > *", {{strokeDasharray: 1, strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: 0.45, ease: "power2.inOut"}}, {hl["t"]});')
        cues.append(dict(t=t0 + hl["t"] + 0.05, snd="draw", gain=-16))
    # focus rings on the dive point, then the exit
    L.append(f'<div id="{sid}-ring1" class="{sid}-ring" style="left:{dx - 90}px;top:{dy - 90}px"></div>')
    L.append(f'<div id="{sid}-ring2" class="{sid}-ring" style="left:{dx - 90}px;top:{dy - 90}px"></div>')
    J.append(f'tl.fromTo("#{sid}-ring1", {{scale: 0.2, opacity: 1}}, {{scale: 1.9, opacity: 0, duration: 0.5, ease: "power2.out", immediateRender: false}}, {D - 0.9:.2f});')
    J.append(f'tl.fromTo("#{sid}-ring2", {{scale: 0.2, opacity: 1}}, {{scale: 1.9, opacity: 0, duration: 0.5, ease: "power2.out", immediateRender: false}}, {D - 0.72:.2f});')
    cues.append(dict(t=t0 + D - 0.88, snd="ping", gain=-17))
    # RGB copies of the finished slide, used by the glitch exit
    L.append(f'<img id="{sid}-rgb-r" class="{sid}-full {sid}-rgb" src="assets/slides/{sc["slide"]}.jpg" alt="" style="filter:grayscale(1) sepia(1) saturate(12) hue-rotate(-45deg)" />')
    L.append(f'<img id="{sid}-rgb-c" class="{sid}-full {sid}-rgb" src="assets/slides/{sc["slide"]}.jpg" alt="" style="filter:grayscale(1) sepia(1) saturate(12) hue-rotate(150deg)" />')
    ex = sc["exit"]
    if ex in ("dive", "glitch"):
        J.append(f'tl.to("#{sid}-cam", {{scale: 7, filter: "blur(16px)", duration: 0.45, ease: "power3.in"}}, {D - 0.45:.2f});')
        cues.append(dict(t=t0 + D, snd="whoosh", gain=-9, align="peak"))
        if ex == "glitch":
            J.append(f'tl.fromTo("#{sid}-rgb-r", {{opacity: 0, x: 0}}, {{opacity: 0.28, x: 22, duration: 0.12, ease: "steps(3)", immediateRender: false}}, {D - 0.36:.2f});')
            J.append(f'tl.fromTo("#{sid}-rgb-c", {{opacity: 0, x: 0}}, {{opacity: 0.28, x: -22, duration: 0.12, ease: "steps(3)", immediateRender: false}}, {D - 0.36:.2f});')
            J.append(f'jitter(tl, "#{sid}-shake", {D - 0.36:.2f});')
            cues.append(dict(t=t0 + D - 0.36, snd="glitch", gain=-12))
    elif ex == "whipL":
        J.append(f'tl.to("#{sid}-cam", {{x: -1150, filter: "blur(18px)", duration: 0.32, ease: "power3.in"}}, {D - 0.32:.2f});')
        cues.append(dict(t=t0 + D, snd="whip", gain=-9, align="peak"))
    elif ex == "whipU":
        J.append(f'tl.to("#{sid}-cam", {{y: -2000, filter: "blur(18px)", duration: 0.32, ease: "power3.in"}}, {D - 0.32:.2f});')
        cues.append(dict(t=t0 + D, snd="whip", gain=-9, align="peak"))
    en = sc["enter"]
    if en == "zoom":
        J.insert(0, 'tl.fromTo("#%s-cam", {scale: 1.45, filter: "blur(14px)"}, {scale: 1, filter: "blur(0px)", duration: 0.5, ease: "expo.out"}, 0);' % sid)
        J.insert(1, 'tl.fromTo("#%s-flash", {opacity: 0.9}, {opacity: 0, duration: 0.22, ease: "power2.out"}, 0);' % sid)
    elif en == "whipL":
        J.insert(0, 'tl.fromTo("#%s-cam", {x: 620, filter: "blur(18px)"}, {x: 0, filter: "blur(0px)", duration: 0.42, ease: "expo.out"}, 0);' % sid)
    elif en == "whipU":
        J.insert(0, 'tl.fromTo("#%s-cam", {y: 1100, filter: "blur(18px)"}, {y: 0, filter: "blur(0px)", duration: 0.42, ease: "expo.out"}, 0);' % sid)
    else:
        pass
    return f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; background: #ffffff; }}
    #{sid}-cam, #{sid}-shake {{ position: absolute; inset: 0; }}
    #{sid}-cam {{ transform-origin: {dx}px {dy}px; }}
    .{sid}-full {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; }}
    .{sid}-lyr {{ position: absolute; }}
    .{sid}-lyr img {{ position: absolute; left: 0; top: 0; display: block; }}
    .{sid}-rgb {{ mix-blend-mode: multiply; z-index: 70; opacity: 0; }}
    .{sid}-spark {{ position: absolute; z-index: 65; opacity: 0; border-radius: 2px; }}
    .{sid}-ring {{ position: absolute; width: 180px; height: 180px; border-radius: 50%; border: 9px solid {BLUE}; z-index: 66; opacity: 0; }}
    #{sid}-sweep {{ position: absolute; z-index: 64; overflow: hidden; }}
    #{sid}-sweep-bar {{ position: absolute; top: 0; left: 0; width: 40%; height: 100%;
      background: linear-gradient(100deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.85) 50%, rgba(255,255,255,0) 100%); }}
    #{sid}-pop, #{sid}-flash {{ position: absolute; inset: 0; background: #ffffff; pointer-events: none; }}
    #{sid}-pop {{ z-index: 80; opacity: 0; }}
    #{sid}-flash {{ z-index: 90; opacity: 0; }}
    {chr(10).join("    " + c for c in css)}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}" data-layout-allow-overflow data-layout-allow-overlap>
    <div id="{sid}-cam">
      <div id="{sid}-shake">
        {chr(10).join("        " + l for l in L)}
        <div id="{sid}-sweep"><div id="{sid}-sweep-bar"></div></div>
      </div>
    </div>
    <div id="{sid}-pop"></div>
    <div id="{sid}-flash"></div>
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      const SX = {SHAKE_X}, SY = {SHAKE_Y};
      function shake(tl, sel, t, amp) {{
        for (let i = 0; i < SX.length; i++) {{
          const k = 1 - i / SX.length;
          tl.to(sel, {{ x: amp * SX[i] * k, y: amp * SY[i] * k, duration: 0.035, ease: "none" }}, t + i * 0.035);
        }}
        tl.to(sel, {{ x: 0, y: 0, duration: 0.05, ease: "power1.out" }}, t + SX.length * 0.035);
      }}
      function jitter(tl, sel, t) {{
        const J = [[-26, 8], [22, -10], [-14, 12], [30, -6], [0, 0]];
        J.forEach((p, i) => tl.to(sel, {{ x: p[0], y: p[1], duration: 0.04, ease: "none" }}, t + i * 0.05));
      }}
{chr(10).join("      " + j for j in J)}
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""

def end_html(cues, t0):
    D = END["dur"]
    return f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; background: #000000; }}
    #end-cam {{ position: absolute; inset: 0; transform-origin: 540px 800px; }}
    #end-logo {{ position: absolute; left: 110px; top: 590px; width: 860px; height: 406px; }}
    #end-logo img {{ width: 100%; height: 100%; display: block; }}
    #end-shine {{ position: absolute; left: 110px; top: 590px; width: 860px; height: 406px; overflow: hidden;
      -webkit-mask-image: url(assets/otm_logo.png); mask-image: url(assets/otm_logo.png);
      -webkit-mask-size: 100% 100%; mask-size: 100% 100%; }}
    #end-shine-bar {{ position: absolute; top: 0; left: 0; width: 35%; height: 100%;
      background: linear-gradient(100deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.95) 50%, rgba(255,255,255,0) 100%); }}
    #end-follow {{ position: absolute; left: 0; width: {W}px; top: 1090px; text-align: center;
      font-family: "Archivo Black", sans-serif; font-size: 92px; letter-spacing: 0.02em; color: #ffffff; line-height: 1.05; }}
    #end-follow span {{ color: {BLUE}; }}
    #end-foot {{ position: absolute; left: 0; top: 1665px; width: {W}px; height: 255px; overflow: hidden; }}
    #end-foot img {{ width: {W}px; height: 255px; display: block; }}
    #end-flash {{ position: absolute; inset: 0; background: #ffffff; opacity: 0; z-index: 9; }}
  </style>
  <div id="root" data-composition-id="end" data-width="{W}" data-height="{H}" data-layout-allow-overflow>
    <div id="end-cam">
      <div id="end-logo"><img src="assets/otm_logo.png" alt="Order the Market" /></div>
      <div id="end-shine"><div id="end-shine-bar"></div></div>
      <div id="end-follow">FOLLOW FOR <span>MORE</span></div>
      <div id="end-foot"><img id="end-foot-img" src="assets/plates/footer.jpg" alt="" /></div>
    </div>
    <div id="end-flash"></div>
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#end-cam", {{ scale: 1.5, filter: "blur(14px)" }}, {{ scale: 1, filter: "blur(0px)", duration: 0.5, ease: "expo.out" }}, 0);
      tl.fromTo("#end-flash", {{ opacity: 0.9 }}, {{ opacity: 0, duration: 0.25, ease: "power2.out" }}, 0);
      tl.fromTo("#end-logo", {{ opacity: 0, scale: 2.4, filter: "blur(16px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.5, ease: "expo.out" }}, 0.2);
      tl.fromTo("#end-flash", {{ opacity: 0.6 }}, {{ opacity: 0, duration: 0.2, ease: "power2.out", immediateRender: false }}, 0.32);
      tl.fromTo("#end-shine-bar", {{ xPercent: -120 }}, {{ xPercent: 320, duration: 0.9, ease: "power2.inOut" }}, 0.75);
      tl.fromTo("#end-follow", {{ clipPath: "inset(0% 100% 0% 0%)", x: -30 }}, {{ clipPath: "inset(0% 0% 0% 0%)", x: 0, duration: 0.5, ease: "power3.out" }}, 1.1);
      tl.fromTo("#end-foot-img", {{ y: 255 }}, {{ y: 0, duration: 0.55, ease: "back.out(1.2)" }}, 1.4);
      window.__timelines["end"] = tl;
    }})();
  </script>
</template>
"""

def main():
    cues = []
    t = 0.0
    hosts = []
    for i, sc in enumerate(SCENES):
        boxes = cut(sc)
        with open(f"{ROOT}/compositions/{sc['id']}.html", "w") as f:
            f.write(scene_html(sc, boxes, cues, t))
        hosts.append((sc["id"], t, sc["dur"]))
        if "vo_start" in sc:
            cues.append(dict(t=t + sc["vo_start"], snd="vo", file=f"vo_{sc['id']}", gain=0))
        t += sc["dur"]
    # the end card's footer: the handles bar from slide 2
    Image.open(f"{ROOT}/assets/slides/s2_what.jpg").crop((0, 1665, 1080, 1920)).save(f"{ROOT}/assets/plates/footer.jpg", quality=92)
    with open(f"{ROOT}/compositions/end.html", "w") as f:
        f.write(end_html(cues, t))
    hosts.append(("end", t, END["dur"]))
    if "vo_start" in END:
        cues.append(dict(t=t + END["vo_start"] + 0.9, snd="vo", file="vo_end", gain=0))
    cues.append(dict(t=t + 0.22, snd="riser", gain=-12, align="end"))
    cues.append(dict(t=t + 0.22, snd="impact", gain=-6))
    cues.append(dict(t=t + 0.75, snd="sting", gain=-10))
    cues.append(dict(t=t + 1.1, snd="tick", gain=-18))
    cues.append(dict(t=t + 1.42, snd="rise", gain=-15))
    cues.append(dict(t=0.04, snd="impact", gain=-5))
    total = round(t + END["dur"], 2)
    host_tags = "\n".join(
        f'      <div id="{hid}" data-composition-id="{hid}" data-composition-src="compositions/{hid}.html" data-start="{s:.2f}" '
        f'data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>'
        for hid, s, d in hosts)
    index = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #ffffff; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="{W}" data-height="{H}" data-motion-blur="on">
{host_tags}
      <audio id="soundtrack" class="clip" src="assets/audio/mix.wav" data-start="0" data-duration="{total}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    with open(f"{ROOT}/index.html", "w") as f:
        f.write(index)
    with open(f"{ROOT}/work/cues.json", "w") as f:
        json.dump(dict(total=total, cues=sorted(cues, key=lambda c: c["t"])), f, indent=1)
    print("total", total, "s,", len(cues), "sound cues, scenes:", [h[0] for h in hosts])

if __name__ == "__main__":
    main()
