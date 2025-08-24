import os, json, datetime, html, pathlib, re, xml.etree.ElementTree as ET
from urllib.parse import quote

SITE = os.getenv("SITE_BASE_URL","https://magazin.tvojehnizdo.com").rstrip("/")
ROOT = pathlib.Path(".")
ARTDIR = ROOT / "articles"
ARTDIR.mkdir(exist_ok=True)

def slugify(s:str)->str:
    s = re.sub(r"\s+", "-", (s or "").strip().lower())
    s = re.sub(r"[^a-z0-9\-]", "", s)
    s = re.sub(r"-+", "-", s)
    return s[:120] or "clanek"

# načti články
arts=[]
if (ROOT/"articles.json").exists():
    try:
        raw=json.load(open(ROOT/"articles.json",encoding="utf-8"))
        arts = raw if isinstance(raw,list) else raw.get("articles",[])
    except Exception: arts=[]

# normalizace + doplnění údajů
for a in arts:
    a.setdefault("title","Článek")
    a["slug"] = a.get("slug") or slugify(a["title"])
    a["date"] = a.get("date") or datetime.date.today().isoformat()
    a.setdefault("excerpt","")
    a.setdefault("author","Tvoje Hnízdo")
    a.setdefault("hero_image","/banner.jpg")
    a.setdefault("tags",[])

# --- vygeneruj detailové stránky
ARTICLE_TMPL = """<!doctype html><html lang="cs"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title} – Magazín Tvoje Hnízdo</title>
<meta name="description" content="{desc}"/>
<link rel="stylesheet" href="/style.css"/>
<link rel="canonical" href="{url}"/>
<meta property="og:title" content="{title}"/><meta property="og:description" content="{desc}"/>
<meta property="og:type" content="article"/><meta property="og:image" content="{image}"/><meta property="og:url" content="{url}"/>
<script type="application/ld+json">
{jsonld}
</script>
</head><body>
<header class="container"><div class="hero"><div class="logo"></div><div><a href="/" class="muted">← zpět</a><h1>{title}</h1><div class="muted">{date} • {author}</div></div></div></header>
<main class="container article">
  <img src="{image}" alt="{title}" />
  <article>
  {body}
  </article>
</main>
<footer class="container">© 2025 Tvoje Hnízdo</footer>
</body></html>"""

def article_jsonld(a, url):
    return json.dumps({
      "@context":"https://schema.org","@type":"Article",
      "headline":a["title"],"description":a["excerpt"],"image":[a["hero_image"]],
      "datePublished":a["date"],"author":{"@type":"Person","name":a["author"]},
      "mainEntityOfPage":{"@type":"WebPage","@id":url}
    }, ensure_ascii=False)

for a in arts:
    url = f"{SITE}/articles/{a['slug']}.html"
    body = a.get("content_html") or f"<p>{html.escape(a['excerpt'])}</p>"
    out = ARTICLE_TMPL.format(
        title=html.escape(a["title"]), desc=html.escape(a["excerpt"]),
        image=html.escape(a["hero_image"]), url=url,
        date=a["date"], author=html.escape(a["author"]),
        body=body, jsonld=article_jsonld(a,url)
    )
    (ARTDIR/f"{a['slug']}.html").write_text(out,encoding="utf-8")

# --- index (SEO varianta, bez JS renderu; rychlý listing)
CARD = lambda a: f'''<article class="card">
  <a href="/articles/{a["slug"]}.html">
    <img class="cover" src="{a["hero_image"]}" alt="{html.escape(a["title"])}">
    <div class="card-body">
      <div class="card-meta">{a["date"]} • {' • '.join(a.get("tags",[])[:3])}</div>
      <h2 class="card-title">{html.escape(a["title"])}</h2>
      <p class="card-excerpt">{html.escape(a["excerpt"])}</p>
    </div>
  </a>
</article>'''
grid = "\n".join(CARD(a) for a in arts)
INDEX = f"""<!doctype html><html lang="cs"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Magazín Tvoje Hnízdo – dřevostavby, inspirace, postupy</title>
<meta name="description" content="Nejnovější články o dřevostavbách: návody, rozpočty, legislativa, inspirace a reálné zkušenosti."/>
<link rel="stylesheet" href="/style.css"/><link rel="alternate" type="application/rss+xml" title="RSS" href="/rss.xml"/>
<link rel="canonical" href="{SITE}/"/><meta property="og:title" content="Magazín Tvoje Hnízdo"/>
<meta property="og:description" content="Návody, inspirace a novinky o dřevostavbách."/><meta property="og:type" content="website"/>
<meta property="og:url" content="{SITE}/"/><meta property="og:image" content="/banner.jpg"/>
</head><body>
<header class="container"><div class="hero"><div class="logo"></div><div><h1>Magazín Tvoje Hnízdo</h1><div class="muted">Dřevostavby • postupy • inspirace • legislativa</div></div></div></header>
<main class="container"><section class="grid">{grid}</section></main>
<footer class="container">© 2025 Tvoje Hnízdo • <a href="/sitemap.xml">sitemap</a> • <a href="/rss.xml">rss</a></footer>
</body></html>"""
(ROOT/"index.html").write_text(INDEX,encoding="utf-8")

# --- sitemap + rss
urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
def add(u):
    uel=ET.SubElement(urlset,"url")
    ET.SubElement(uel,"loc").text=u
    ET.SubElement(uel,"lastmod").text=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    ET.SubElement(uel,"changefreq").text="daily"
    ET.SubElement(uel,"priority").text="0.8"
add(f"{SITE}/")
for a in arts: add(f"{SITE}/articles/{a['slug']}.html")
ET.ElementTree(urlset).write("sitemap.xml",encoding="utf-8",xml_declaration=True)

rss = ET.Element("rss", version="2.0"); ch = ET.SubElement(rss,"channel")
ET.SubElement(ch,"title").text="Tvoje Hnízdo – Magazín"; ET.SubElement(ch,"link").text=f"{SITE}/"
ET.SubElement(ch,"description").text="Novinky a články o dřevostavbách a bydlení."
ET.SubElement(ch,"lastBuildDate").text=datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
for a in arts[:100]:
    it=ET.SubElement(ch,"item")
    ET.SubElement(it,"title").text=a["title"]
    link=f"{SITE}/articles/{a['slug']}.html"
    ET.SubElement(it,"link").text=link
    ET.SubElement(it,"guid").text=link
    ET.SubElement(it,"description").text=a["excerpt"]
ET.ElementTree(rss).write("rss.xml",encoding="utf-8",xml_declaration=True)
print("OK: built articles + feeds")