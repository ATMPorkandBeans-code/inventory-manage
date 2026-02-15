from flask import Flask, jsonify, request
from services import get_product_info


app = Flask(__name__)

products = []

@app.route("/")
def hello_world():
    return "<p>Welcome to the Inventory Managememt API!</p>"

@app.route("/products/<barcode>", methods=["GET"])
def get_product_route(barcode):
    product = [p for p in products if p["barcode"] == barcode]
    if not product:
        return "Product at barcode does not exist"
    return jsonify(product)

@app.route("/products", methods=["GET"])
def get_all_products_route():
    if products:
        return jsonify([p for p in products])
    else:
        return ("No Products saved to Inventory")

@app.route("/products", methods=["POST"])
def add_product():
    data = request.json
    api_data = get_product_info(data["name"])

    product_id = len(products) + 1

    new_product = {
        "id": product_id,
        "name": data["name"],
        "brand": api_data["brand"],
        "ingredients": api_data["ingredients"],
        "price": data["price"],
        "stock": data["stock"],
        "barcode": api_data["barcode"]
    }
    products.append(new_product)

    return jsonify(new_product), 201

@app.route("/products/<id>", methods=["PATCH"])
def update_project(id):
    data = request.get_json()
    product = ((p for p in products if p["id"] == id), None)
    if not product:
        return ("Product not found", 404)
    product["price"] = data["price"]
    return jsonify(product)




if __name__ == "__main__":
    app.run(debug=True)


