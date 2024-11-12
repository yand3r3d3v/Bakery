from products import Bread, Pizza, Product
from employee import Baker, Kassir, Boss, Barista

class Client:
    def __init__(self, name: str, money: int):
        self.name= name
        self.money = money

class Purchase():
    def __init__(self, products: dict[Product, int]):
        self.products = products

class Bakery:
    def __init__(self, name=None, describe=None, employes=None, productions = None):
        self.name = name
        self.descirbe = describe
        self.employes = employes
        self.productions = productions
        self.category = (Bread, Pizza)
    
    def enough_money(self, client_money, cnt, product_price):
        if client_money >= product_price * cnt:
            return True
        return False
    
    def show_menu(self):
        print('Наш ассортимент!')
        for category in self.category:
            print(f'{category.name}:')
            for product in self.productions:
                if isinstance(product, category):
                    print(f'- {product.name} (В наличии {product.count}) {product.price} руб.')

    def product_exists(self, product_name):
        return any(True for product in self.productions if product_name == product.name)
    
    def product_enough(self, product, cnt):
        return product.count >= cnt

    def choose_products(self):
        products = dict()
        product_choose = str(input('Введите наименование продукта: ')).lower()
        while product_choose != 'думаю хватит':
            if self.product_exists(product_choose):
                product = [product for product in self.productions if product_choose == product.name][0]
                count = int(input('Введите желаемое кол-во продукции: '))
                if self.product_enough(product=product, cnt=count):
                    products.setdefault(product, count)    
            product_choose = str(input('Введите наименование продукта: ')).lower()
        
        return Purchase(products)


        

if __name__ == '__main__':
    # СОЗДАЕМ ПРОДУКЦИЮ
    white_bread = Bread('1', 10, 1000)
    black_bread = Bread('ч. хлеб', 10, 1000)
    rzanoy_bread = Bread('ржаной хлеб', 10, 10000)
    peperoni = Pizza('Пеперони', 10, 10000)
    gawaia = Pizza('Гавайская', 10, 10000)


    # СОЗДАЕМ СОТРУДНИКОВ
    barista = Barista('Кирилл', 1_000_000)
    baker = Baker('Саша', 1_000_001)
    kassir = Kassir('Влад', 999_999)

    # ИНИЦИАЛИЗАЦИЯ ПЕКАРНИ
    bakery = Bakery(name='Пирожки', employes=[barista, baker, kassir],productions=[white_bread, black_bread, peperoni])

    # НАЧАЛО ВЗАИМОДЕЙСТВИЯ
    name, money = 'Витя', 10000
    #name = input('Введите имя: ')
    #money = int('Сколько у вас денег: ')
    print(f'ДОБРО ПОЖАЛОВАТЬ В ПЕКАРНЮ {bakery.name} {name}!')
    if bakery.descirbe is not None:
        print(bakery.descirbe)

    # ПРОДОЛЖЕНИЕ ВЗАИМОДЕЙСТВИЯ
    #bakery.show_menu()
    purchase = bakery.choose_products()
    print(purchase.products)