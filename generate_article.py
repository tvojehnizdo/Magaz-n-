import openai
import os
import json
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

today = datetime.today().strftime('%Y-%m-%d')
title = "Jak postavit dům svépomocí: První kroky"
summary = "Začínáte se stavbou svépomocí? Přečtěte si, jak začít a čemu se vyhnout."
prompt = f"Napiš článek v češtině s názvem '{title}' pro blog o dřevostavbách. Měl by být profesionální, čtivý, a obsahovat praktické rady."

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Jsi odborný redaktor českého magazínu o dřevostavbách."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7
)

article_html = f"<html><head><meta charset='UTF-8'><title>{title}</title><link rel='stylesheet' href='../css/style.css'></head><body><h1>{title}</h1><p><em>{today}</em></p><article>{response['choices'][0]['message']['content'].replace('\n', '<br>')}</article></body></html>"

# Save article
filename = f"{today}-jak-postavit-dum-svepomoci.html"
with open(f"articles/{filename}", "w", encoding="utf-8") as f:
    f.write(article_html)

# Update JSON index
article_entry = {
    "title": title,
    "summary": summary,
    "filename": filename
}

if os.path.exists("articles.json"):
    with open("articles.json", "r", encoding="utf-8") as f:
        articles = json.load(f)
else:
    articles = []

articles.insert(0, article_entry)

with open("articles.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)
