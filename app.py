from flask import Flask, jsonify
from product import Product
from storage import get_product, save_product, get_all_products
from services import fetch_from_openfoodfacts


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Welcome to the Inventory Managememt API!</p>"

@app.route("/products/<barcode>", methods=["GET"])
def get_product_route(barcode):
    product = get_product(barcode)

    if product:
        return jsonify(product.to_dict())
    
    external_data = fetch_from_openfoodfacts(barcode)

    if not external_data:
        return jsonify({"error": "Product not found"}), 404
    
    new_product = Product(**external_data)
    save_product(new_product)

    return jsonify(new_product.to_dict())

@app.route("/products", methods=["GET"])
def get_all_products_route():
    products = get_all_products()
    if products:
        return jsonify([p.to_dict() for p in products()])
    else:
        return ("No Products saved to Inventory")

@app.route("/products", methods=["POST"])
def add_new_product(barcode):
    external_data = fetch_from_openfoodfacts(barcode)
    new_product = Product(**external_data)
    return jsonify(new_product.to_dict())
    


if __name__ == "__main__":
    app.run(debug=True)

