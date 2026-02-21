import requests

BASE_URL = "http://127.0.0.1:5000"

def add_product():
    name = input("Enter product name: \n")
    while True:
        try:
            price = float(input(f"Enter a price per unit for {name}: \n"))
            if price > 0 and price:
                formatted_price = (f"{price:.2f}")
                print(f"Price is set at {formatted_price}.")
                break
            else:
                print(f"Price must be a positive number")
                continue
        except ValueError:
            print("Price must be a positive number")
            continue
        
    while True:
        try:
            stock = int(input(f"How many units would you like to stock for {name}: \n"))
            if stock > 0:
                print(f"Stock is set at {stock}.\nSaving product, one moment...")
                break
            else:
                print("Stock must be a positive integer")
        except ValueError:
            print("Stock must be a positive integer")
            continue

    try:
        response = requests.post(f"{BASE_URL}/products", json={"name": name, "price": formatted_price, "stock": stock})
        print(format_response(response.json()))
    except requests.exceptions.HTTPError:
        print(f"Server Error: {response.json().get('error', 'Critical failure')}")
    except Exception as e:
        print(f"Connection failed: {e}")

def view_all_products():
    print("\nCurrent Inventory: \n")
    try:
        response = requests.get(f"{BASE_URL}/products")
        response.raise_for_status()
        for product in response.json():
            print(format_response(product))
    except requests.exceptions.RequestException as e:
        print("Error:", e)

def view_product():
    barcode = validate_barcode()
    try:
        response = requests.get(f"{BASE_URL}/products/{barcode}")
        response.raise_for_status()
        parsed_response = response.json()
        if not parsed_response:
            print("No product found.")
            return
        print(format_response(parsed_response[0]))
    except requests.exceptions.HTTPError:
        print("Server returned error:")
        print(response.json())

    except requests.exceptions.ConnectionError:
        print("Could not connect to Flask server.")

    except requests.exceptions.RequestException as e:
        print("Unexpected error:", e)


def edit_product():
    id = validate_barcode()
    user_input = input("Would you like to update the item's price or stock? Type price/stock\n")
    if user_input == "price":
        while True:
            try:
                price = float(input(f"What would you like to update the price to? \n"))
                if price > 0 and price:
                    formatted_price = (f"{price:.2f}")
                    payload = {"id": id, "price": formatted_price}
                    print(f"Updated price is set at {formatted_price}")
                    break
                else:
                    print("Price must be a positive number")
                    continue
            except ValueError:
                print("Price must be a positive number")
                continue
            
        try:
            response = requests.patch(f"{BASE_URL}/products/{id}", json = payload)
            print(format_response(response.json()))
        except requests.exceptions.HTTPError:
            print("Server error:", response.json())
        except requests.exceptions.ConnectionError:
            print("Cannot connect to server.")
        except requests.exceptions.RequestException as e:
            print("Unexpected error:", e)


    elif user_input == "stock":
        while True:
            try:
                stock = int(input(f"What would you like to update the stock to? \n"))
                if stock > 0 and stock:
                    payload = {"id": id, "stock": stock}
                    print(f"Updtaed stock is set at {stock}")
                    break
                else:
                    print("Stock must be a positive number")
                    continue
            except ValueError:
                ("Stock must be a positive number")
                continue



        try:
            response = requests.patch(f"{BASE_URL}/products/{id}", json = payload)
            print(format_response(response.json()))
        except requests.exceptions.HTTPError:
            print("Server error:", response.json())
        except requests.exceptions.ConnectionError:
            print("Cannot connect to server.")
        except requests.exceptions.RequestException as e:
            print("Unexpected error:", e)
    
    else:
        print("Could not understand request...please try again.")

def delete_product():
    id = validate_barcode()
    user_input = input("Are you sure you would like to delete this product? yes/no \n")

    if user_input == "yes":
        try: 
            url = f"{BASE_URL}/products/{id}"
            response = requests.delete(url)
            response.raise_for_status()
            print(response.json())
        except requests.exceptions.HTTPError:
            print("Server returned an error:", response.text)
        except requests.exceptions.ConnectionError:
            print("Could not connect to server.")
    
    else:
        print("Please choose another option")
        

def format_response(product):
    p = product["product"]

    ingredients_string = p.get("ingredients", "No ingredients listed")
    split_ingredients = [i.strip() for i in ingredients_string.split(",")]

    formatted_ingredients = "\n".join(f"  - {ingredient}" for ingredient in split_ingredients)

    return (
        f"\n"
        f"Name: {p.get('name', 'N/A')}\n"
        f"Brand: {p.get('brand', 'N/A')}\n\n"
        f"Ingredients:\n"
        f"{formatted_ingredients}\n\n"
        f"Price: {p.get('price', 'N/A')}\n"
        f"Stock: {p.get('stock', 'N/A')}\n"
        f"ID/Barcode: {p.get('barcode', 'N/A')}\n"
    )

def validate_barcode():
    while True:
        try:
            barcode = str(input("Please Enter the ID/Barcode of the Product: \n"))
            if type(barcode) == str and len(barcode) == 13:
                return barcode
            else:
                print("Barcode must be a positive integer and 13 characters")
                continue
        except ValueError:
            print("Barcode must be a positive integer and 13 characters")
            continue



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