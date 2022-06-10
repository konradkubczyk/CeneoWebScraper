import os
import re
import json
import requests
import matplotlib
from app import app
from app.models.product import Product
from flask import render_template, redirect, url_for, request

matplotlib.use('Agg')

@app.errorhandler(404)
def error_404(error):
    return render_template("error.html", error={"title": "Strona nie istnieje", "description": "Strona o podanym adresie nie została odnaleziona."}), 404

@app.route('/')
def index():
    return render_template("index.html.jinja")

@app.route('/extract', methods=['POST', 'GET'])
def extract():
    if request.method == "POST":
        product_id = re.search("\d+", request.form['product_id']).group()
        assert(requests.get(f"https://www.ceneo.pl/{product_id}#tab=reviews").ok)
        
        product = Product(product_id)
        product.extract_name()
        if product.product_name:
            product.extract_opinions().calculate_stats().draw_charts()
        else:
            return render_template("error.html", error={"title": "Nieprawidłowy produkt", "description": "Produkt o podanym identyfikatorze lub adresie nie jest dostępny."}), 400

        # if len(all_opinions) == 0:
        #     return render_template("error.html", error={"title": "Brak opinii", "description": "Produkt nie posiada żadnych opinii."}), 400
        
        return redirect(url_for('product', product_id=product_id))
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
    
    return render_template("product.html.jinja", product_id=product_id, stats=stats, opinions=opinions)