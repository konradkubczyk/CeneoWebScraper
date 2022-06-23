from flask import Flask
from app.gatekeeper import launch

launch()

app = Flask(__name__)

from app import routes

app.run(debug=True)