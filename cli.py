import requests
from app import products

BASE_URL = "http://127.0.0.1:5000"

def add_product():
    name = input("Enter product name: ")
    price = float(input(f"Enter a price per unit for {name}: "))
    stock = int(input(f"How many units would you like to stock for {name}: "))
    response = requests.post(f"{BASE_URL}/products", json={"name": name, "price": price, "stock": stock})
    print(response.json())

def view_all_products():
    response = requests.get(f"{BASE_URL}/products")
    print(response.json())

def view_product():
    barcode = int(input("Please Enter the Barcode for the Product: "))
    response = requests.get(f"{BASE_URL}/products/{barcode}")
    print(response.json())

def edit_product():
    id = int(input("Please Enter the Product's ID number: "))
    # product = (p for p in products if product["id"] == product_id)
    # if not product:
    #     print("Product id not found")
    # product_name = product["name"]
    # id = product["id"]
    # user_input = input(f"""Would you like to edit: \n
    #                    1. {product_name} price 
    #                    2. {product_name} stock
    #                     """)
    # if user_input == "1":
    price = float(input(f"What would you like to update the price to?"))
    response = requests.patch(f"{BASE_URL}/products/{id}", json = {"price": price})
    print(response.json())

while True:
    user_input = input("""Would you like to: \n
                       1. Add a Product\n
                       2. View the existing Inventory\n
                       3. View existing product by Barcode\n
                       4. Edit product price or stock\n
                       4. Quit:\n""")
    if user_input == "1":
        add_product()

    elif user_input == "2":
        view_all_products()

    elif user_input =="3":
        view_product()
        
    elif user_input == "4":
        edit_product()

    elif user_input == "5":
        break