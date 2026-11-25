# Copies the signal bot's reader (supabase/functions/tg-signals/parse.js) into website/js/sigparse.js for the lot calculator.
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
p = root / "website/js/sigparse.js"
s = p.read_text()
head, tail = s.split("(function (root) {\n", 1)
body = (root / "supabase/functions/tg-signals/parse.js").read_text().replace("export function", "function")
p.write_text(head + "(function (root) {\n" + body + '\n  root.OTMParse = { parseSignal, parseTargets, parseResult, mentionedSymbol };\n})(typeof window !== "undefined" ? window : globalThis);\n')
print("website/js/sigparse.js updated")
