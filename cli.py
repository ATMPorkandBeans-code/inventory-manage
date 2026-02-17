import requests

BASE_URL = "http://127.0.0.1:5000"

def add_product():
    name = input("Enter product name: \n")
    price = float(input(f"Enter a price per unit for {name}: \n"))
    stock = int(input(f"How many units would you like to stock for {name}: \n"))
    response = requests.post(f"{BASE_URL}/products", json={"name": name, "price": price, "stock": stock})
    print(response.json())

def view_all_products():
    response = requests.get(f"{BASE_URL}/products")
    print(response.json())

def view_product():
    barcode = int(input("Please Enter the Barcode for the Product: \n"))
    response = requests.get(f"{BASE_URL}/products/{barcode}")
    print(response.json())

def edit_product():
    id = int(input("Please Enter the Product's ID number: \n"))
    user_input = input("Would you like to update the item's price or stock? \n")
    if user_input == "price":
        price = float(input(f"What would you like to update the price to? \n"))
        payload = {"id": id, "price": price}
        response = requests.patch(f"{BASE_URL}/products/{id}", json = payload)
        print(response.json())
    elif user_input == "stock":
        stock = float(input(f"What would you like to update the stock to? \n"))
        payload = {"id": id, "stock": stock}
        response = requests.patch(f"{BASE_URL}/products/{id}", json = payload)
        print(response.json())

def delete_product():
    id = int(input("Please enter the Product's ID number to delete: \n"))
    user_input = input("Are you sure you would like to delete this product? yes/no \n")

    if user_input == "yes": 
        url = f"{BASE_URL}/products/{id}"
        response = requests.delete(url)
        print(response.json())


while True:
    user_input = input("""Would you like to: \n
                       1. Add a Product\n
                       2. View the existing Inventory\n
                       3. View existing product by Barcode\n
                       4. Edit product price or stock\n
                       5. Delete a Product\n
                       6. Quit:\n""")
    if user_input == "1":
        add_product()

    elif user_input == "2":
        view_all_products()

    elif user_input =="3":
        view_product()
        
    elif user_input == "4":
        edit_product()

    elif user_input == "5":
        delete_product()

    elif user_input == "6":
        break