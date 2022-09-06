from flask import Blueprint
from flask import render_template, jsonify


index_bp = Blueprint('index',__name__)



@index_bp.route("/", methods = ["GET","POST"])
def home():
    return render_template("dashboard.html")


@index_bp.route("/precos", methods = ["GET","POST"])
def sellers_prices():
    return render_template("precos.html")