#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

# Flask application in flask_app.py provides a response content type of application/json at "/bakeries" 
@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    response = make_response(
        bakeries,
        200
    )
    return response
# Flask application in flask_app.py provides a response content type of application/json at "/bakeries/<int:id>"
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_dict = bakery.to_dict()
    response = make_response(
        bakery_dict,
        200
    )
    return response

# Flask application in flask_app.py provides a response content type of application/json at "/baked_goods/by_price"
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # baked_goods_by_prices = []
    # for baked_goods_by_price in BakedGood.query.all():
    #     baked_prices_dict = {
    #         "id": baked_goods_by_price.id,
    #         "name": baked_goods_by_price.name,
    #         "price": baked_goods_by_price.price
    #     }
    #     baked_goods_by_prices.append(baked_prices_dict)
    #     response = make_response(
    #         jsonify(baked_goods_by_prices),
    #         200
    #     )
    # return response
     # Get all baked goods sorted by price in descending order
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()

    # Convert baked goods to list of dictionaries
    baked_goods_dicts = [baked_good.to_dict() for baked_good in baked_goods]

    # Create JSON response
    response = make_response(
        jsonify(baked_goods_dicts),
        200
    )

    return response

#  Flask application in flask_app.py provides a response content type of application/json at "/bakeries/<int:id>"
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if most_expensive:
        baked_good_dict = most_expensive.to_dict()

        response = make_response(
            jsonify(baked_good_dict),
            200
        )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
