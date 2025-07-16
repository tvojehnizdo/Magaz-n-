# Magazín Tvoje Hnízdo

Profesionální online magazín pro web [TvojeHnizdo.cz](https://tvojehnizdo.cz) zaměřený na dřevostavby, inspiraci a rady pro budoucí majitele domů.

---

## 📌 Funkce

- 🧠 Automatické generování článků 1× týdně pomocí GPT-4
- 🌐 Nasazení na GitHub Pages (statický web)
- 🎨 Moderní design, banner a barvy značky
- 🔗 Tlačítka pro sdílení: Facebook, LinkedIn, Zkopírovat odkaz
- 📄 Každý článek jako samostatný HTML soubor

---

## 🚀 Nasazení

1. Vytvoř si nový repozitář na GitHubu, např. `tvojehnizdo-magazin`
2. Nahraj všechny soubory ze ZIP balíčku
3. V nastavení repozitáře aktivuj GitHub Pages:
   - **Settings → Pages → Branch: `main`, Folder: `/ (root)`**
4. Vytvoř GitHub Secret:
   - `Settings → Secrets → Actions → New repository secret`
   - Jméno: `OPENAI_API_KEY`
   - Hodnota: *tvůj OpenAI klíč*

Výsledný web poběží na adrese např.:  
`https://uzivatel.github.io/tvojehnizdo-magazin`

---

## 🤖 Automatizace

Pomocí GitHub Actions (`.github/workflows/generate-article.yml`) se každý **týden (pondělí 9:00)** automaticky vygeneruje nový článek a nahraje do složky `articles/`.

Používá se OpenAI GPT-4 a šablonový skript v `scripts/generate_article.py`.

---

## 📁 Struktura projektu

```
tvojehnizdo-magazin/
├── index.html                  # Hlavní stránka magazínu
├── articles/                   # Složka s jednotlivými články
├── css/style.css               # Vzhled magazínu
├── assets/banner.jpg           # Grafický banner
├── articles.json               # Přehled článků
├── scripts/generate_article.py # GPT skript pro generování článků
└── .github/workflows/generate-article.yml # GitHub Action pro automatizaci
```

---

## 🔧 Budoucí možnosti rozšíření

- Newsletter (automatická rozesílka článků)
- RSS feed
- Kategorie a filtrování článků
- Fulltextové vyhledávání
- Překlad článků (EN, DE)

---

© 2025 [Tvoje Hnízdo](https://tvojehnizdo.cz)
