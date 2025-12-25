from flask import Flask, session, request, jsonify, render_template
from flask_session import Session
import requests

app = Flask(__name__)

app.secret_key = "supersecretkey"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

PRODUCT_API = "https://dummyjson.com/products"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/products")
def products():
    r = requests.get(PRODUCT_API)
    return jsonify(r.json()["products"][:8])

@app.route("/api/cart", methods=["POST"])
def add_to_cart():
    if "cart" not in session:
        session["cart"] = []

    product = request.json.get("product")
    session["cart"].append(product)
    session.modified = True

    return jsonify(session["cart"])

@app.route("/api/cart")
def get_cart():
    return jsonify(session.get("cart", []))
