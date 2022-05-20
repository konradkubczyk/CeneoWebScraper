from app import app
from flask import render_template

@app.route('/')
@app.route('/index/<name>')
def index(name="Hello World!"):
    return render_template("index.html", text=name)

@app.errorhandler(404)
def error_404(error):
    return "Strona o podanym adresie nie została odnaleziona. :(", 404