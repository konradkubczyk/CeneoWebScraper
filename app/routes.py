import os
import re
import json
import requests
import selectors
import numpy as np
from app import app
import pandas as pd
from tkinter import Y
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from flask import render_template, redirect, url_for, request

def get_item(ancestor, selector, attribute=None, return_list=False):
    try:
        if return_list:
            return [item.get_text().strip() for item in ancestor.select(selector)]
        if attribute:
            return ancestor.select_one(selector)[attribute]
        return ancestor.select_one(selector).get_text().strip()
    except (AttributeError, TypeError):
        return None

selectors = {
    "author": ["span.user-post__author-name"],
    "recommendation": ["span.user-post__author-recomendation > em"],
    "stars": ["span.user-post__score-count"],
    "content": ["div.user-post__text"],
    "useful": ["button.vote-yes > span"],
    "useless": ["button.vote-no > span"],
    "published": ["span.user-post__published > time:nth-child(1)", "datetime"],
    "purchased": ["span.user-post__published > time:nth-child(2)", "datetime"],
    "pros": ["div[class$=positives] ~ div.review-feature__item", None, True],
    "cons": ["div[class$=negatives] ~ div.review-feature__item", None, True]
}

@app.errorhandler(404)
def error_404(error):
    return render_template("error.html", error={"title": "Strona nie istnieje", "description": "Strona o podanym adresie nie została odnaleziona."}), 404

@app.route('/')
def index():
    return render_template("index.html.jinja")

@app.route('/extract', methods=['POST', 'GET'])
def extract():
    if request.method == "POST":
        try:
            product_id = re.search("\d+", request.form['product_id']).group()
            assert(requests.get(f"https://www.ceneo.pl/{product_id}#tab=reviews").ok)
            url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
            
            all_opinions = []

            while(url):
                response = requests.get(url)
                page = BeautifulSoup(response.text, "html.parser")
                opinions = page.select("div.js_product-review")

                for opinion in opinions:
                    single_opinion = {
                        key:get_item(opinion, *value)
                            for key, value in selectors.items()
                    }
                    single_opinion["opinion_id"] = opinion["data-entry-id"]
                    all_opinions.append(single_opinion)
                
                try:
                    url = "https://www.ceneo.pl" + page.select_one("a.pagination__next")["href"]
                except TypeError:
                    url = None

            if not os.path.exists(f"app/opinions"):
                os.makedirs("app/opinions")

            with open(f"app/opinions/{product_id}.json", "w", encoding="UTF-8") as jfile:
                json.dump(all_opinions, jfile, indent=4, ensure_ascii=False)
            
            return redirect(url_for('product', product_id=product_id))
        except (AttributeError, AssertionError):
            return render_template("error.html", error={"title": "Nieprawidłowy produkt", "description": "Produkt o podanym identyfikatorze lub adresie nie jest dostępny."}), 400
        return render_template("error.html", error={"title": "Błąd serwera", "description": "Wystąpił błąd serwera."}), 500
    else:
        return render_template("extract.html.jinja")

@app.route('/products')
def products():
    products = [filename.split(".")[0] for filename in os.listdir("app/opinions")]
    return render_template("products.html.jinja", products=products)

@app.route('/author')
def author():
    return render_template("author.html.jinja")

@app.route('/product/<product_id>')
def product(product_id):
    opinions = pd.read_json(f"opinions/{product_id}.json")
    opinions["stars"] = opinions["stars"].map(lambda x: float(x.split("/")[0].replace(",", ".")))

    stats = {
        "opinions_count": len(opinions),
        "pros_count": opinions["pros"].map(bool).sum(),
        "cons_count": opinions["cons"].map(bool).sum(),
        "average_score": opinions["stars"].mean().round(2)
    }

    if not os.path.exists(f"app/opinions"):
        os.makedirs("app/opinions")

    recommendation = opinions["recommendation"].value_counts(dropna=False).sort_index().reindex(["Nie polecam", "Polecam", None], fill_value=0)
    recommendation.plot.pie(
        label = "",
        autopct = lambda p: "{:.1f}%".format(round(p)) if p > 0 else "",
        colors = ["crimson", "forestgreen", "lightskyblue"],
        labels = ["Nie polecam", "Polecam", "Nie mam zdania"]
    )

    plt.title("Rekomendacje")
    plt.savefig(f"app/plots/{product_id}_recommendations.png")
    plt.close()

    stars = opinions["stars"].value_counts().sort_index().reindex(list(np.arange(0, 5.5, 0.5)), fill_value=0)
    stars.plot.bar(
        color = "pink"
    )
    plt.title("Oceny produktu")
    plt.xlabel("Liczba gwiazdek")
    plt.ylabel("Liczba opinii")
    plt.grid(True, axis=Y)
    plt.xticks(rotation=0)
    plt.savefig(f"app/plots/{product_id}_stars.png")
    plt.close()
    return render_template("product.html.jinja", product_id=product_id, stats=stats, opinions=opinions)