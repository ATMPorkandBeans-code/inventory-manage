class Product():
    def __init__(self, barcode, name, brand, calories):
        self.barcode = barcode
        self.name = name
        self.brand = brand
        self.calories = calories

    def to_dict(self):
        return {"barcode": self.barcode,
                "name": self.name,
                "brand": self.brand,
                "calories": self.calories}