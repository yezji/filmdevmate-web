"""ko/ja 페이지 생성기.

출력은 순수 정적 HTML 이다. 이 스크립트는 배포 파이프라인이 아니라 **문안을 한
곳에서 관리하기 위한 도구**다 — 페이지 뼈대가 같은 글이 언어마다 네 벌씩이라,
손으로 복사해 두면 한 군데 고칠 때 열두 군데가 어긋난다. 생성 결과도 저장소에
그대로 커밋하므로 GitHub Pages 는 이 파일을 알 필요가 없다.

    python3 build_i18n.py

영어(루트)는 손으로 쓴 원본이라 건드리지 않는다.
"""
import html, json, os

BASE = "https://yezji.github.io/filmdevmate-web"
LOCALES = ("ko", "ja")
PAGES = ("", "dilution", "temperature", "steps")

NAV = {
    'ko': {'': 'FilmDevMate', 'dilution': '희석 계산', 'temperature': '온도', 'steps': '공정 순서'},
    'ja': {'': 'FilmDevMate', 'dilution': '希釈計算', 'temperature': '温度', 'steps': '工程順'},
}
LANGNAME = {'en': 'English', 'ko': '한국어', 'ja': '日本語'}
CREDITS = {'ko': '크레딧', 'ja': 'クレジット'}
LOCALE = {'en': 'en_US', 'ko': 'ko_KR', 'ja': 'ja_JP'}
OG_ALT = {
    'ko': "현상 단계에 9분 21초가 남아 있는 FilmDevMate 타이머 화면.",
    'ja': "現像工程に9分21秒が残っている FilmDevMate のタイマー画面。",
}
DOWNLOAD = {'ko': '다운로드', 'ja': '入手'}


def page(lang, slug, title, desc, body, jsonld):
    depth = 2 if slug else 1
    up = "../" * depth
    canon = f"{BASE}/{lang}/" + (f"{slug}/" if slug else "")
    alts = "".join(
        f'\n<link rel="alternate" hreflang="{l}" href="{BASE}/' +
        (f'{l}/' if l != 'en' else '') + (f'{slug}/' if slug else '') + '">'
        for l in ('en', 'ko', 'ja'))
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{BASE}/' + (f'{slug}/' if slug else '') + '">'

    switch = " · ".join(
        f'<a href="{BASE}/' + (f'{l}/' if l != 'en' else '') + (f'{slug}/' if slug else '') + f'">{LANGNAME[l]}</a>'
        if l != lang else f'<span>{LANGNAME[l]}</span>'
        for l in ('en', 'ko', 'ja'))

    crumb = (f'<p class="breadcrumb"><a href="../">{NAV[lang][""]}</a> / {NAV[lang][slug]}</p>'
             if slug else '')
    home = "../" if slug else "./"
    chrome = (f'<div class="chrome">\n'
              f'  <b><a href="{home}" aria-label="FilmDevMate">'
              f'<img class="mark" src="{up}img/mark.png" alt="" width="123" height="128">FilmDevMate</a></b>\n'
              f'  <nav>'
              f'<a href="{home}dilution/">{NAV[lang]["dilution"]}</a>'
              f'<a href="{home}steps/">{NAV[lang]["steps"]}</a>'
              f'<a href="#get">{DOWNLOAD[lang]}</a>'
              f'</nav>\n</div>')
    # SEO. og:url 은 canonical 과 반드시 같은 값이어야 한다.
    alt_locales = "".join(
        f'<meta property="og:locale:alternate" content="{LOCALE[l]}">\n'
        for l in ('en', 'ko', 'ja') if l != lang)
    seo = f"""<meta property="og:type" content="website">
<meta property="og:site_name" content="FilmDevMate">
<meta property="og:locale" content="{LOCALE[lang]}">
{alt_locales}<meta property="og:url" content="{canon}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{BASE}/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{OG_ALT[lang]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{BASE}/img/og.jpg">
<meta name="theme-color" content="#0b0f0e">
<link rel="icon" href="{up}favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="{up}img/apple-touch-icon.png">
"""

    # 하위 면에는 BreadcrumbList, 첫 면에는 WebSite.
    home = f"{BASE}/{lang}/"
    if slug:
        jsonld = list(jsonld) + [{
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "FilmDevMate", "item": home},
                {"@type": "ListItem", "position": 2, "name": NAV[lang][slug], "item": f"{home}{slug}/"}]}]
    else:
        jsonld = list(jsonld) + [{
            "@context": "https://schema.org", "@type": "WebSite", "name": "FilmDevMate",
            "url": home, "inLanguage": lang,
            "sameAs": ["https://www.instagram.com/filmdevmate/"],
            "publisher": {"@type": "Person", "name": "Yeji Hong"}}]

    scripts = "\n".join(
        '<script type="application/ld+json">\n' +
        json.dumps(d, ensure_ascii=False, indent=2) + '\n</script>' for d in jsonld)

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">{alts}
{seo}<link rel="stylesheet" href="{up}style.css">
{scripts}
</head>
<body>
{chrome}
<div class="wrap">
{crumb}
{body}
<footer>\n  <p><a href="{home}credits/">{CREDITS[lang]}</a> &middot; <a href="https://www.instagram.com/filmdevmate/" rel="me noopener">@filmdevmate</a></p>\n  <p class="langswitch">{switch}</p></footer>
</div>
</body>
</html>
"""


def write(lang, slug, doc):
    d = os.path.join(lang, slug) if slug else lang
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w').write(doc)
    print('  wrote', os.path.join(d, 'index.html'))
