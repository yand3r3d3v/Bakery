class Product:
    def __init__(self, name, count, price, time):
        self.name = name
        self.count = count
        self.price = price
        self.time = time

class Bread(Product):
    name = 'Хлеб'

class Pizza(Product):
    name = 'Пицца'
