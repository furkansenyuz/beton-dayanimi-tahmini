"""furkan_demo_body.html + furkan_model.json -> artifact + standalone"""
import pathlib
D = pathlib.Path(__file__).parent
body = (D / "furkan_demo_body.html").read_text(encoding="utf-8")
model = (D / "furkan_model.json").read_text(encoding="utf-8")
assert "/*__MODEL__*/" in body
icerik = body.replace("/*__MODEL__*/", model)
(D / "furkan_demo_artifact.html").write_text(icerik, encoding="utf-8")
son = icerik.index("</title>") + len("</title>")
baslik, govde = icerik[:son], icerik[son:].lstrip()
html = f"""<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Beton karisim recetesinden basinc dayanimi tahmini. Random forest modeli tarayicida calisir.">
  {baslik}
  <style>
    *, *::before, *::after {{ box-sizing: border-box; }}
    * {{ margin: 0; }}
    img, svg {{ display: block; max-width: 100%; }}
    button, input, select, summary {{ font: inherit; color: inherit; }}
    h1, h2, h3 {{ font-weight: inherit; font-size: inherit; }}
  </style>
</head>
<body>
{govde}
</body>
</html>
"""
out = pathlib.Path("/home/user/senasayginsenyuz/furkan-beton-dayanimi-tahmini/demo/index.html")
out.write_text(html, encoding="utf-8")
print(f"artifact {len(icerik)//1024} KB | standalone {len(html)//1024} KB -> {out}")
