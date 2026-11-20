// Minimal .xlsx reader for the browser: no library, no upload. Reads the zip with DecompressionStream
// and the sheets with DOMParser, and returns { sheetName: [[cell, ...], ...] } (values only).
(function (root) {
  const u16 = (b, o) => b[o] | (b[o + 1] << 8);
  const u32 = (b, o) => (b[o] | (b[o + 1] << 8) | (b[o + 2] << 16) | (b[o + 3] << 24)) >>> 0;
  const dec = new TextDecoder();

  async function inflate(bytes) {
    const ds = new DecompressionStream("deflate-raw");
    const out = new Response(new Blob([bytes]).stream().pipeThrough(ds));
    return new Uint8Array(await out.arrayBuffer());
  }

  // zip directory -> { name: async () => Uint8Array }
  function unzip(buf) {
    const b = new Uint8Array(buf);
    let eocd = -1;
    for (let i = b.length - 22; i >= Math.max(0, b.length - 65557); i--) if (u32(b, i) === 0x06054b50) { eocd = i; break; }
    if (eocd < 0) throw new Error("not-xlsx");
    const count = u16(b, eocd + 10);
    let p = u32(b, eocd + 16);
    const files = {};
    for (let n = 0; n < count; n++) {
      if (u32(b, p) !== 0x02014b50) throw new Error("not-xlsx");
      const method = u16(b, p + 10), size = u32(b, p + 20), nameLen = u16(b, p + 28), extraLen = u16(b, p + 30), commentLen = u16(b, p + 32);
      const local = u32(b, p + 42);
      const name = dec.decode(b.subarray(p + 46, p + 46 + nameLen));
      files[name] = async () => {
        const start = local + 30 + u16(b, local + 26) + u16(b, local + 28);
        const raw = b.subarray(start, start + size);
        return method === 8 ? inflate(raw) : raw;
      };
      p += 46 + nameLen + extraLen + commentLen;
    }
    return files;
  }

  const xml = async (files, name) => (files[name] ? new DOMParser().parseFromString(dec.decode(await files[name]()), "application/xml") : null);
  const byTag = (node, tag) => [...node.getElementsByTagName(tag)];
  const colIndex = (ref) => { let n = 0; for (const ch of ref.replace(/\d+$/, "")) n = n * 26 + (ch.charCodeAt(0) - 64); return n - 1; };

  async function read(file) {
    const files = unzip(await file.arrayBuffer());
    const wb = await xml(files, "xl/workbook.xml");
    if (!wb) throw new Error("not-xlsx");
    const rels = await xml(files, "xl/_rels/workbook.xml.rels");
    const target = {};
    if (rels) byTag(rels, "Relationship").forEach((r) => { target[r.getAttribute("Id")] = r.getAttribute("Target"); });
    const ss = await xml(files, "xl/sharedStrings.xml");
    const strings = ss ? byTag(ss, "si").map((si) => byTag(si, "t").map((x) => x.textContent).join("")) : [];
    const out = {};
    for (const sh of byTag(wb, "sheet")) {
      const rid = sh.getAttribute("r:id") || sh.getAttributeNS("http://schemas.openxmlformats.org/officeDocument/2006/relationships", "id");
      let path = target[rid] || "";
      path = path.startsWith("/") ? path.slice(1) : "xl/" + path.replace(/^\.\//, "");
      const doc = await xml(files, path);
      if (!doc) continue;
      const rows = [];
      for (const row of byTag(doc, "row")) {
        const cells = [];
        for (const c of byTag(row, "c")) {
          const ty = c.getAttribute("t"), v = c.getElementsByTagName("v")[0];
          let val = null;
          if (ty === "s") val = v ? strings[+v.textContent] : null;
          else if (ty === "inlineStr") val = byTag(c, "t").map((x) => x.textContent).join("");
          else if (ty === "str" || ty === "e") val = v ? v.textContent : null;
          else if (ty === "b") val = v ? v.textContent === "1" : null;
          else val = v ? (isNaN(+v.textContent) ? v.textContent : +v.textContent) : null;
          const ref = c.getAttribute("r");
          cells[ref ? colIndex(ref) : cells.length] = val;
        }
        for (let i = 0; i < cells.length; i++) if (cells[i] === undefined) cells[i] = null;
        if (cells.some((x) => x !== null && x !== "")) rows.push(cells);
      }
      out[sh.getAttribute("name")] = rows;
    }
    return out;
  }

  root.OTMXlsx = { read };
})(window);
