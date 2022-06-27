import re
import math
import json
import matplotlib
import pandas as pd
from app import app
from app.models.product import Product
from app.models.database import Database
from flask import render_template, redirect, url_for, request, Response

matplotlib.use('Agg')

@app.errorhandler(404)
def error_404(error):
    return render_template("error.html", error={"title": "Strona nie istnieje", "description": "Strona o podanym adresie nie została odnaleziona."}), 404

@app.route('/')
def index():
    libraries = []
    for file in ["requirements.txt", "libraries.txt"]:
        with open(file, "r") as tfile:
            entries = tfile.readlines()
            for entry in entries:
                libraries.append('<li>' + entry.replace('==', ' <span class="badge text-bg-light">') + '</span></li>')
    return render_template("index.html.jinja", libraries=libraries)

@app.route('/extract', methods=['POST', 'GET'])
def extract():
    if request.method == "POST":
        return direct_extract(request.form['product_id'])
    else:
        return render_template("extract.html.jinja")

@app.route('/extract/<product_id>')
def direct_extract(product_id):
    try:
        product_id = re.search("\d+", product_id).group()
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
        # Remove any previous content associated with this product ID before saving new data
        product.delete_product()
        product.draw_charts()
        product.export_opinions()
        product.export_product()
    else:
        error = "Nie udało się pobrać danych produktu o podanym identyfikatorze."
        return render_template("extract.html.jinja", error=error)        
    return redirect(url_for('product', product_id=product_id))

@app.route('/products')
def products():
    db = Database()
    query = f"SELECT * FROM `products`;"
    cnx = db.connect()
    cnx.database = db.database
    cursor = cnx.cursor()
    cursor.execute(query)
    product_ids = []
    for product in cursor:
        product_ids.append(product[0])
    products = []
    for product_id in product_ids:
        product = Product(product_id)
        product.import_product()
        product.average_rating = "%.2f" % round(product.average_score, 2)
        product.full_stars = math.floor(product.average_score)
        if product.average_score - product.full_stars >= 0.75:
            product.full_stars += 1
        product.half_star = product.average_score - product.full_stars >= 0.25
        product.empty_stars = 5 - (product.full_stars + product.half_star)
        products.append(product)
    return render_template("products.html.jinja", products=products)

@app.route('/author')
def author():
    return render_template("author.html.jinja")

@app.route('/product/<product_id>')
def product(product_id):
    product = Product(product_id)
    product.import_product()
    opinions_json = json.dumps(product.opinions_to_dict()).replace("'", "&rsquo;")
    print(opinions_json)
    return render_template("product.html.jinja", product=product, opinions_json=opinions_json)

@app.route("/product/<product_id>/get-opinions/<format>")
def download_product(product_id, format):
    product = Product(product_id)
    product.import_product()
    if format == "csv":
        opinions_df = product.opinions_to_df()
        csv_object = pd.DataFrame.to_csv(opinions_df)
        return Response(csv_object, mimetype="text/csv", headers={"Content-Disposition": f"attachment; filename={product_id}_opinions.csv"})
    if format == "json":
        opinions_dict = product.opinions_to_dict()
        json_object = json.dumps(opinions_dict, indent=4, ensure_ascii=False)
        return Response(json_object, mimetype="application/json", headers={"Content-Disposition": f"attachment; filename={product_id}_opinions.json"})
    if format == "xml":
        return Response(product.opinions_to_xml(), mimetype="application/xml", headers={"Content-Disposition": f"attachment; filename={product_id}_opinions.xml"})

@app.route("/product/<product_id>/delete")
def delete_product(product_id):
    product = Product(product_id)
    product.import_product()
    product.delete_product()
    return redirect(url_for('products'))