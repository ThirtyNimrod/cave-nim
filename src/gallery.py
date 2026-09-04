import html as html_lib

_STYLE = """
  body { background:#121316; color:#D8DCE0; font-family:sans-serif; margin:0; padding:24px; }
  h1 { font-weight:400; }
  .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:16px; }
  .card { background:#1b1d21; border-radius:8px; overflow:hidden; }
  .card img { width:100%; display:block; }
  .meta { padding:10px 12px; font-size:14px; }
  .meta p { opacity:.75; margin:6px 0 0; }
"""


def _card_html(entry: dict) -> str:
    lines = "<br>".join(html_lib.escape(line) for line in entry["lines"])
    return f"""
        <div class="card">
          <img src="{html_lib.escape(entry['image_path'])}" alt="{html_lib.escape(entry['id'])}">
          <div class="meta">
            <strong>{html_lib.escape(entry['id'])}</strong> — {html_lib.escape(entry['icon'])} / {html_lib.escape(entry['theme'])}
            <p>{lines}</p>
          </div>
        </div>"""


def build_gallery_html(entries: list[dict]) -> str:
    cards = "".join(_card_html(e) for e in reversed(entries))
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>nim. gallery</title>
<style>{_STYLE}</style>
</head>
<body>
<h1>nim. — {len(entries)} posts</h1>
<div class="grid">{cards}
</div>
</body>
</html>
"""
