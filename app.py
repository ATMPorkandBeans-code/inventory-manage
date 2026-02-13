from flask import Flask, jsonify, request
from item import Item

app = Flask(__name__)

storage_array = [
    Item(1, "Bananas", 3, 60),
    Item(2, "Apple Pie", 18.99, 20)
]

@app.route("/")
def hello_world():
    return "<p>Welcome to the Inventory Managememt API!</p>"


@app.route("/items", methods=["GET"])
def get_items():
    data = [i.to_dict() for i in storage_array]
    return jsonify(data)

@app.route("/items/<int:id>", methods=["GET"])
def get_product(id):
    item = next((i for i in storage_array if i.id == id), None)
    return jsonify(item.to_dict() if item else ("Item not found"))

@app.route("/items", methods = ["GET"])
def create_item():
    data = request.get_json()
    new_id = max((i.id for i in storage_array), default=0) + 1
    new_item = Item(id=new_id, name=data["name"], price=data["price"], stock=data["stock"])
    storage_array.append(new_item)
    return jsonify(new_item.to_dict())



if __name__ == "__main__":
    app.run(debug=True)

