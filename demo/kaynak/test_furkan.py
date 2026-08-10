from playwright.sync_api import sync_playwright
import pathlib, json, subprocess
URL = pathlib.Path("/home/user/senasayginsenyuz/furkan-beton-dayanimi-tahmini/demo/index.html").as_uri()
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
hatalar = []

def oku(p):
    return p.evaluate("""() => {
      const t = id => document.getElementById(id).textContent.trim();
      const cells = [...document.querySelectorAll('.sinif-cell')];
      return {mpa:t('mpa'), mpaU:t('mpa-u'), alt:t('mpa-alt'), verdict:t('verdict'),
              aciklama:t('aciklama'), sc:t('sc-v'), age:t('age-v'), cement:t('cement-v'),
              cementU:document.querySelector('.u-doz').textContent.trim(),
              caption:t('unit-caption'), sinif:(cells.find(c=>c.dataset.simdiki==='1')||{}).textContent,
              siniflar:cells.map(c=>c.textContent), egri:document.getElementById('egri-cizgi').getAttribute('d').slice(0,40)};
    }""")

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
    p = b.new_page(viewport={"width":1280,"height":1500}, color_scheme="light")
    js=[]; p.on("pageerror", lambda e: js.append(str(e)))
    p.on("console", lambda m: js.append(m.text) if m.type=="error" else None)
    p.goto(URL); p.wait_for_timeout(700)
    if js: hatalar.append(f"JS hatasi: {js}")

    print("SENARYOLAR:")
    for ad in ["Tipik yapısal beton","Yüksek dayanımlı","Az çimentolu karışım","Genç beton","Cüruf ve kül katkılı","Modelin şaştığı numune"]:
        p.click(f'button.scn:has-text("{ad}")'); p.wait_for_timeout(1150)
        r = oku(p)
        print(f"  {ad:22s} {r['mpa']:>6s} {r['mpaU']:4s} ({r['alt']:>10s})  s/c={r['sc']}  sinif={r['sinif']}  {r['verdict']}")
        print(f"       > {r['aciklama'][:118]}")

    # genc beton senaryosunda 28 gun projeksiyonu var mi
    p.click('button.scn:has-text("Genç beton")'); p.wait_for_timeout(1150)
    if "28. günde" not in oku(p)["aciklama"]:
        hatalar.append("genc betonda 28 gun projeksiyonu gorunmuyor")

    # birim degisimi tahmini bozmamali (MPa <-> psi orani sabit)
    p.click('button.scn:has-text("Tipik yapısal beton")'); p.wait_for_timeout(1150)
    ab = oku(p)
    p.click('input[name="unit"][value="US"]'); p.wait_for_timeout(400)
    us = oku(p)
    mpa_ab, psi_us = float(ab["mpa"]), float(us["mpa"])
    if abs(psi_us/145.0377 - mpa_ab) > 0.15:
        hatalar.append(f"birim cevrimi tutarsiz: {mpa_ab} MPa vs {psi_us} psi")
    if not (us["mpaU"]=="psi" and us["cementU"]=="lb/yd³"):
        hatalar.append(f"birim etiketleri: {us['mpaU']} / {us['cementU']}")
    # sinif merdiveni TS EN 206-1 kartinda oldugu icin birim seciminden bagimsiz, hep EN sinifi
    if us["siniflar"][0] != "C16/20": hatalar.append(f"sinif merdiveni EN sinifi degil: {us['siniflar']}")
    print(f"\nBIRIM: AB {ab['mpa']} {ab['mpaU']} cim={ab['cement']} {ab['cementU']} sinif={ab['sinif']}")
    print(f"       ABD {us['mpa']} {us['mpaU']} cim={us['cement']} {us['cementU']} sinif={us['sinif']}")

    for _ in range(6):
        p.click('input[name="unit"][value="AB"]'); p.click('input[name="unit"][value="US"]')
    p.click('input[name="unit"][value="AB"]'); p.wait_for_timeout(300)
    geri = oku(p)
    for k in ("mpa","cement","sc","age"):
        if ab[k]!=geri[k]: hatalar.append(f"6 gecis sonrasi {k} kaydi: {ab[k]} -> {geri[k]}")

    # yas kaydiricisi egriyi ve imleci hareket ettiriyor mu
    p.evaluate("() => {const s=document.getElementById('age'); s.value=365; s.dispatchEvent(new Event('input'));}")
    p.wait_for_timeout(300); y365 = oku(p)
    p.evaluate("() => {const s=document.getElementById('age'); s.value=1; s.dispatchEvent(new Event('input'));}")
    p.wait_for_timeout(300); y1 = oku(p)
    if float(y365["mpa"]) <= float(y1["mpa"]):
        hatalar.append(f"yas artinca dayanim artmadi: 1gun={y1['mpa']} 365gun={y365['mpa']}")
    print(f"YAS ETKISI: 1 gun={y1['mpa']} MPa -> 365 gun={y365['mpa']} MPa")

    # agrega bolumu acilip kapaniyor mu
    p.click("details.ekstra summary"); p.wait_for_timeout(200)
    if not p.is_visible("#coarseagg"): hatalar.append("agrega bolumu acilmadi")

    p.click('button.scn:has-text("Tipik yapısal beton")'); p.wait_for_timeout(1150)
    if p.evaluate("() => document.documentElement.scrollWidth > window.innerWidth + 1"):
        hatalar.append("masaustu yatay tasma")
    p.screenshot(path="f_light.png", full_page=True); p.close()

    d = b.new_page(viewport={"width":1280,"height":1500}, color_scheme="dark")
    d.goto(URL); d.wait_for_timeout(700)
    d.click('button.scn:has-text("Yüksek dayanımlı")'); d.wait_for_timeout(1150)
    d.screenshot(path="f_dark.png", full_page=True); d.close()

    m = b.new_page(viewport={"width":390,"height":844}, color_scheme="light")
    m.goto(URL); m.wait_for_timeout(700)
    m.click('button.scn:has-text("Genç beton")'); m.wait_for_timeout(1150)
    if m.evaluate("() => document.documentElement.scrollWidth > window.innerWidth + 1"):
        hatalar.append("mobil yatay tasma")
    m.screenshot(path="f_mobil.png"); m.close()

    dar = b.new_page(viewport={"width":320,"height":700}); dar.goto(URL); dar.wait_for_timeout(500)
    if dar.evaluate("() => document.documentElement.scrollWidth > window.innerWidth + 1"):
        hatalar.append("320px yatay tasma")
    dar.close(); b.close()

print("\n" + ("TUM TESTLER GECTI" if not hatalar else "SORUNLAR:\n  " + "\n  ".join(hatalar)))
