import requests


def get_product_info(product_name):
    search_url = "https://world.openfoodfacts.org/cgi/search.pl"

    search_params = {
        "search_terms": product_name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1,
        "fields": "code"
    }
    search_response = requests.get(search_url, params=search_params)
    search_data = search_response.json()

    products = search_data.get("products")
    if not products:
        return {"error": "No products found."}

    barcode = products[0]["code"]

    product_url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"

    product_response = requests.get(product_url)
    product_data = product_response.json().get("product", {})

    brand = product_data.get("brands", "Brand not available")


    ingredients = (
        product_data.get("ingredients_text_en")
        or product_data.get("ingredients_text")
        or "Ingredients not available"
    )

    return {
        "product_name": product_data.get("product_name", product_name),
        "brand": brand,
        "ingredients": ingredients,
        "barcode": barcode
    }


