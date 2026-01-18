from flask import Flask, jsonify, request
from models import db, Restaurant, Pizza, RestaurantPizza

@app.route("/restaurants")
def restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([
        r.to_dict(only=("id", "name", "address"))
        for r in restaurants
    ])
@app.route("/restaurants/<int:id>")
def restaurant_by_id(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    return jsonify(
        restaurant.to_dict(
            include={
                "restaurant_pizzas": {
                    "only": ("id", "price", "pizza_id", "restaurant_id", "pizza")
                }
            }
        )
    )
@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    db.session.delete(restaurant)
    db.session.commit()
    return "", 204
@app.route("/pizzas")
def pizzas():
    pizzas = Pizza.query.all()
    return jsonify([
        p.to_dict(only=("id", "name", "ingredients"))
        for p in pizzas
    ])
@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()

    try:
        rp = RestaurantPizza(
            price=data["price"],
            restaurant_id=data["restaurant_id"],
            pizza_id=data["pizza_id"]
        )
        db.session.add(rp)
        db.session.commit()

        return jsonify(
            rp.to_dict(
                include={
                    "pizza": {},
                    "restaurant": {}
                }
            )
        ), 201

    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400
