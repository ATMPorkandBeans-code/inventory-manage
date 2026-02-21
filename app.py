from flask import Flask, jsonify, request
from services import get_product_info

app = Flask(__name__)

products = []

@app.route("/")
def hello_world():
    return "<p>Welcome to the Inventory Managememt API!</p>"

@app.route("/products/<barcode>", methods=["GET"])
def get_product_route(barcode):
    try:
        product = [p for p in products if p["product"]["barcode"] == barcode]
        return jsonify(product)
    except IndexError:
        return jsonify({"error": "Product not found"}), 404

@app.route("/products", methods=["GET"])
def get_all_products_route():
    return jsonify(products), 200
 
@app.route("/products", methods=["POST"])
def add_product():
    data = request.json
    try:
        api_data = get_product_info(data["name"])

        for product in products:
            if product["id"] == api_data["barcode"]:
                return jsonify("Product already exists in Inventory.")

        new_product = {
            "id": api_data["barcode"],
            "product": {
            "name": data["name"],
            "brand": api_data["brand"],
            "ingredients": api_data["ingredients"],
            "price": data["price"],
            "stock": data["stock"],
            "barcode": api_data["barcode"]
        }}
        products.append(new_product)

        return jsonify(new_product), 201
    except Exception:
        return jsonify({"error": "Failed to fetch external data. Local array not updated."}), 502


@app.route("/products/<int:id>", methods=["PATCH"])
def update_product(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Empty request body"}), 400
    
    product = next((p for p in products if str(p["id"]) == str(id)), None)
    if not product:
        return ("Product not found", 404)
    
    if "price" in data:
        try:
            product["product"]["price"] = data.get("price")
        except Exception as e:
            return jsonify({"error": "Update failed", "details": str(e)}), 500
        
    elif "stock" in data:
        try:
            product["product"]["stock"] = data.get("stock")
        except Exception as e:
            return jsonify({"error": "Update failed", "details": str(e)}), 500
        
    return jsonify(product)


@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    global products
    try:
        products = [p for p in products if str(p["id"]) != str(id)]
        return jsonify({"message": "Product deleted successfully"}), 200
    except:
        return {"error": "Product not found"}, 404


if __name__ == "__main__":
    app.run(debug=True)


