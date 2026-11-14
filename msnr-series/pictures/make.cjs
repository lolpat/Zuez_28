// Builds the MSNR picture set (1080x1350, Instagram 4:5) from still frames of the episode videos.
// Each slide: the episode frame without captions, scaled to fit, plus one key rule and the handle line.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const DIR = __dirname;
const frames = fs.readFileSync(path.join(DIR, 'frames.txt'), 'utf8').trim().split('\n').map(l => l.split(' '));
const ACC = ['#e0566b', '#f29bb0', '#b3b7ff', '#a6e3a1', '#5ee0c0', '#f5c451', '#c9a0ff', '#8e7cff', '#d6336c'];
const RULES = [
  'Exact levels from candle <b>opens &amp; closes</b>, not wide zones',
  'Price returns to the A-Level &rarr; look for <b>SELLS</b>',
  'Price returns to the V-Level &rarr; look for <b>BUYS</b>',
  'High &rarr; higher high &rarr; MSS.<br><b>Sell the return to the QML</b>',
  'Broken resistance holds as support &rarr; <b>BUY the retest</b>',
  'Broken support holds as resistance &rarr; <b>SELL the retest</b>',
  'Close meets the next open &rarr; draw the <b>OCL</b>',
  'Two touches draw it, <b>the 3rd touch is the trade</b>',
  'Measure the sweep wick: <b>its 50% is the reaction level</b>',
];
const url = p => 'file://' + p;
const HEAD = `<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;800&display=swap" rel="stylesheet">
<style>*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1350px;background:#000;overflow:hidden;font-family:Montserrat,sans-serif;color:#fff}
.crop{position:absolute;overflow:hidden}.crop img{position:absolute;left:0}</style>`;

function slide(i) {
  const [still] = frames[i];
  // source rows 40..1420 (logo through chart) scaled 0.88 into the top of the slide
  const s = 0.85, top = 40, h = 1380;
  return `<!doctype html><html><head>${HEAD}<style>
  .crop{left:${(1080 - 1080 * s) / 2}px;top:6px;width:${1080 * s}px;height:${h * s}px}
  .crop img{width:${1080 * s}px;top:${-top * s}px}
  .rule{position:absolute;left:60px;right:60px;top:1196px;text-align:center;font-weight:800;font-size:35px;line-height:1.25;text-wrap:balance}
  .rule b{color:${ACC[i]}}
  .bar{position:absolute;left:340px;right:340px;top:1180px;height:3px;background:${ACC[i]};border-radius:2px}
  .foot{position:absolute;left:0;right:0;bottom:22px;text-align:center;font-weight:600;font-size:22px;letter-spacing:4px;color:#8a8f99}
  .num{position:absolute;right:34px;top:30px;font-weight:800;font-size:24px;color:#555;letter-spacing:2px}
  </style></head><body>
  <div class="crop"><img src="${url(still)}"></div>
  <div class="bar"></div><div class="rule">${RULES[i]}</div>
  <div class="foot">@FXZUEZ_28 &nbsp;·&nbsp; ORDER THE MARKET</div>
  <div class="num">${i + 1}/10</div></body></html>`;
}

function endSlide() {
  const card = frames[8][1];
  return `<!doctype html><html><head>${HEAD}<style>
  .a{left:0;top:120px;width:1080px;height:760px}.a img{width:1080px;top:-470px}
  .b{left:0;bottom:0;width:1080px;height:190px}.b img{width:1080px;top:-1730px}
  .save{position:absolute;left:0;right:0;top:930px;text-align:center;font-weight:800;font-size:40px}
  .save b{color:#2962ff}
  .sub{position:absolute;left:0;right:0;top:1000px;text-align:center;font-weight:600;font-size:26px;color:#9aa0aa;letter-spacing:2px}
  .num{position:absolute;right:34px;top:30px;font-weight:800;font-size:24px;color:#555;letter-spacing:2px}
  </style></head><body>
  <div class="crop a"><img src="${url(card)}"></div>
  <div class="save">SAVE &amp; <b>SHARE</b> THIS GUIDE</div>
  <div class="sub">Full MSNR video series on the profile</div>
  <div class="crop b"><img src="${url(card)}"></div>
  <div class="num">10/10</div></body></html>`;
}

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  fs.mkdirSync(path.join(DIR, 'out'), { recursive: true });
  const pages = [...frames.map((_, i) => slide(i)), endSlide()];
  for (let i = 0; i < pages.length; i++) {
    const f = path.join(DIR, `tmp_${i}.html`);
    fs.writeFileSync(f, pages[i]);
    await p.goto(url(f), { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(DIR, 'out', `MSNR_${String(i + 1).padStart(2, '0')}.png`) });
  }
  await b.close();
  console.log('ok', pages.length);
})();
