import requests
def fetch_from_openfoodfacts(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)

    if response.status_code != 200:
        return None
    
    data = response.json()

    if data.get("status") != 1:
        return None
    
    product = data["product"]

    return {
        "barcode": barcode,
        "name": product.get("product_name"),
        "brand": product.get("brands"),
        "calories": product.get("nutriments", {}).get("energy-kcal_100g")
    }