import os
import re
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
    libraries = []
    for file in ["libraries.txt", "requirements.txt"]:
        with open(file, "r") as tfile:
            entries = tfile.readlines()
            for entry in entries:
                libraries.append('<li>' + entry.replace('==', ' <span class="badge text-bg-light">') + '</span></li>')
    return render_template("index.html.jinja", libraries=libraries)

@app.route('/extract', methods=['POST', 'GET'])
def extract():
    if request.method == "POST":
        try:
            product_id = re.search("\d+", request.form['product_id']).group()
        except AttributeError:
            error = "Wprowadzona wartość jest niepoprawna."
            return render_template("extract.html.jinja", error=error)
        product = Product(product_id)
        product.extract_name()
        if product.product_name:
            product.extract_opinions()
            # Prevent processing products with no opinions
            if len(product.opinions) == 0:
                error = "Produkt nie posiada opinii, nie można przeprowadzić analizy."
                return render_template("extract.html.jinja", error=error)
            product.calculate_stats()
            product.draw_charts()
            product.export_opinions()
            product.export_product()
        else:
            error = "Nie udało się pobrać produktu o podanym identyfikatorze."
            return render_template("extract.html.jinja", error=error)        
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
    product = Product(product_id)
    product.import_product()
    stats = product.stats_to_dict()
    opinions = product.opinions_to_df()
    return render_template("product.html.jinja", product_id=product_id, stats=stats, opinions=opinions)
