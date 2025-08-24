import os, json, datetime, html, pathlib, re, xml.etree.ElementTree as ET
from urllib.parse import quote
SITE=os.getenv("SITE_BASE_URL","https://magazin.tvojehnizdo.com").rstrip("/")
R=pathlib.Path("."); (R/"articles").mkdir(exist_ok=True)
def slugify(s): s=re.sub(r"\s+","-", (s or "").strip().lower()); s=re.sub(r"[^a-z0-9\-]","",s); return (re.sub(r"-+","-",s) or "clanek")[:120]
try:
  import markdown; MD=True
except:
  MD=False

arts=[]
if (R/"content/seed-articles.json").exists():
  raw=json.load(open(R/"content/seed-articles.json",encoding="utf-8"))
  arts=raw if isinstance(raw,list) else raw.get("articles",[])

for a in arts:
  a.setdefault("title","Článek"); a["slug"]=a.get("slug") or slugify(a["title"])
  a["date"]=a.get("date") or datetime.date.today().isoformat()
  a.setdefault("excerpt",""); a.setdefault("author","Tvoje Hnízdo")
  a.setdefault("hero_image","/banner.jpg"); a.setdefault("tags",[]); a.setdefault("category","")
  if MD and a.get("content_md"): a["content_html"]=markdown.markdown(a["content_md"], extensions=["extra","sane_lists","tables"])

ART_TMPL="""<!doctype html><html lang="cs"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{t} – Magazín Tvoje Hnízdo</title><meta name="description" content="{d}"/>
<link rel="stylesheet" href="/style.css"/><link rel="canonical" href="{u}"/>
<meta property="og:title" content="{t}"/><meta property="og:description" content="{d}"/><meta property="og:type" content="article"/>
<meta property="og:url" content="{u}"/><meta property="og:image" content="{img}"/></head>
<body><header class="container"><a href="/">← Zpět</a></header>
<main class="container article"><h1>{t}</h1><div class="meta">{date} • {author}</div>{hero}<article>{body}</article></main>
<footer class="container">© 2025 Tvoje Hnízdo</footer></body></html>"""
def CARD(a): return f"<article class='card'><a href='/articles/{a['slug']}.html'><img class='cover' src='{a.get('hero_image','/banner.jpg')}' alt='{html.escape(a['title'])}'/><div class='card-body'><div class='card-meta'>{a['date']} • {' • '.join(a.get('tags',[])[:3])}</div><h2 class='card-title'>{html.escape(a['title'])}</h2><p class='card-excerpt'>{html.escape(a['excerpt'])}</p></div></a></article>"

# detail + index
cards=[]
for a in arts:
  url=f"{SITE}/articles/{a['slug']}.html"; body=a.get("content_html") or f"<p>{html.escape(a['excerpt'])}</p>"
  hero=f"<img class='cover' src='{a['hero_image']}' alt='{html.escape(a['title'])}'/>" if a.get("hero_image") else ""
  (R/"articles"/f"{a['slug']}.html").write_text(ART_TMPL.format(t=html.escape(a['title']),d=html.escape(a['excerpt']),u=url,img=a.get("hero_image"),body=body,hero=hero,date=a['date'],author=html.escape(a['author'])),encoding="utf-8")
  cards.append(CARD(a))
R.joinpath("index.html").write_text(f"<!doctype html><meta charset='utf-8'><link rel='stylesheet' href='/style.css'><title>Magazín TH</title><main class='container'><section class='grid'>{''.join(cards)}</section></main>",encoding="utf-8")

# sitemap & rss
u=ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
def add(x): el=ET.SubElement(u,"url"); ET.SubElement(el,"loc").text=x; ET.SubElement(el,"lastmod").text=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
add(SITE+"/"); [add(f"{SITE}/articles/{a['slug']}.html") for a in arts]
ET.ElementTree(u).write("sitemap.xml",encoding="utf-8",xml_declaration=True)
rss=ET.Element("rss",version="2.0"); ch=ET.SubElement(rss,"channel")
ET.SubElement(ch,"title").text="Tvoje Hnízdo – Magazín"; ET.SubElement(ch,"link").text=f"{SITE}/"
ET.SubElement(ch,"description").text="Novinky o dřevostavbách a bydlení."
ET.SubElement(ch,"lastBuildDate").text=datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
for a in arts[:100]:
  it=ET.SubElement(ch,"item"); ET.SubElement(it,"title").text=a["title"]
  link=f"{SITE}/articles/{a['slug']}.html"; ET.SubElement(it,"link").text=link
  ET.SubElement(it,"guid").text=link; ET.SubElement(it,"description").text=a["excerpt"]
ET.ElementTree(rss).write("rss.xml",encoding="utf-8",xml_declaration=True)
print("OK: build complete")
