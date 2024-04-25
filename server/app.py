#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
import requests
import json
from sqlalchemy_serializer import SerializerMixin

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

@app.route('/bakeries')
def bakeries():

    bakeries = []
    for bakery in Bakery.query.all():
        bakery_dict = bakery.to_dict()
        # bakery_dict = {
        #         "id": bakery.id,
        #         "name": bakery.name,
        #         "created_at": bakery.created_at,
        #         "updated_at": bakery.updated_at
        # }
        bakeries.append(bakery_dict)

    response = make_response(
        bakeries,
        200,
        {"Content-Type": "application/json"}
    )

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter(Bakery.id == id).first()

    bakery_dict = {
        "id": bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at,
        "updated_at": bakery.updated_at
    }

    response = make_response(
        bakery_dict,
        200,
        {"Content-Type": "application/json"}
    )

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    bakedgoods = []

    for bakedgood in BakedGood.query.order_by(BakedGood.price.desc()).all():
        bakedgood_dict = bakedgood.to_dict()
        # bakedgood_dict = {
        #     "id": bakedgood.id,
        #     "name": bakedgood.name,
        #     "price": bakedgood.price,
        #     "created_at": bakedgood.created_at,
        #     "updated_at": bakedgood.updated_at
        # }

        bakedgoods.append(bakedgood_dict)

    response = make_response(
        bakedgoods,
        200,
        {"Content-Type": "application/json"}
    )

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).all()[0]
    most_expensive_dict = most_expensive.to_dict()
    response = make_response(
        most_expensive_dict,
        200,
        {"Content-Type": "application/json"}
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
