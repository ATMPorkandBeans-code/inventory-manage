product_store = {}

def get_product(barcode):
    return product_store.get(barcode)

def save_product(product):
    product_store[product.barcode] = product

def get_all_products():
    return list(product_store.values())

