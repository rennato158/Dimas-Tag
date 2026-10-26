#!/usr/bin/env python3
"""Gera public/index.html a partir de src/dimas-tag.html (versão standalone / PWA).
Uso: python3 build.py
"""
import hashlib, pathlib, re
root = pathlib.Path(__file__).parent
src = (root / "src" / "dimas-tag.html").read_text(encoding="utf-8")

# bibliotecas locais em vez de CDN; remove meta específica do artifact
src = src.replace('https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js', 'vendor/jszip.min.js')
src = src.replace('https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js', 'vendor/xlsx.full.min.js')
src = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\n?', '', src)

head = '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0d0d0d">
<meta name="application-name" content="DIMAS Tag">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="DIMAS Tag">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="icons/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
'''
tail = '''
<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));
}
</script>
</body>
</html>
'''
# o <title> e os <link>/<script> do src ficam no head; o resto vai para o body
m = re.search(r'(<style>)', src)
head_part, body_part = src[:m.start()], src[m.start():]
html = head + head_part + "</head>\n<body>\n" + body_part + tail

out = root / "public" / "index.html"
out.write_text(html, encoding="utf-8")

# versão do cache do service worker muda a cada build
digest = hashlib.sha256(html.encode("utf-8")).hexdigest()[:10]
sw = (root / "sw.template.js").read_text(encoding="utf-8").replace("__VERSION__", digest)
(root / "public" / "sw.js").write_text(sw, encoding="utf-8")
print("ok: public/index.html e public/sw.js (versão", digest + ")")
