class Product:
    def __init__(self, name, count, price):
        self.name = name
        self.count = count
        self.price = price

class Bread(Product):
    name = 'Хлеб'

class Pizza(Product):
    name = 'Пицца'
