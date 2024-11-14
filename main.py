import matplotlib.pyplot as plt

from products import Bread, Pizza, Product
from employee import Baker, Kassir, Boss, Barista, Employee

class Client:
    def __init__(self, name: str, money: int):
        self.name= name
        self.money = money

class Bakery:
    def __init__(self, name, products=list[Product], employes=list[Employee]):
        self.name = name
        self.products = products
        self.employes = employes

    def start(self, client: Client):
        plt = self.drow_graph()

        product = self.choose_product()
        cnt = self.choose_count(product=product)
        self.calculate_purchase(product, cnt, client)
        plt.close()


    def calculate_purchase(self, product, cnt, client):
        summary_price = product.price*int(cnt)

        if self.enough_money(product.price*int(cnt), client.money):
            self.show(f'Спасибо за покупку. Вы купили {product.name} за {summary_price} руб.')
            self.change_count(product, int(cnt))
            self.withdraw_money(client, summary_price)
        else: 
            self.show(f'У вас не хватает денег. \n Товар стоит: {summary_price} руб., а у вас {client.money} руб.')

    def choose_product(self):
        while True:
            product = self.ask('Выберите товар, укажите его название: ')
            state, ans, product = self.product_exists(product=product)
            self.show(ans)
            if state:
               break
        return product
    
    def choose_count(self, product):
        while True:
            count = self.ask(f'Выберите кол-во товара (доступно {product.count}): ')
            if self.enough_count(product, count):
                break
            self.show('Извините, но товара не хватает, выберите другое кол-во!')
        return count

    def product_exists(self, product):
        if any(pos for pos in self.products if pos.name == product):
            product = [prod for prod in self.products if prod.name == product][0]
            return True, 'Такой товар есть, какое количество вам нужно?', product
        return False, 'Простите, но такого товара нет, попробуйте еще раз', None

    def enough_count(self, product, cnt):
        if product.count >= int(cnt):
            return True
        return False

    def enough_money(self, product_price, client_money):
        if product_price <= client_money:
            return True
        return False

    def change_count(self, product, cnt):
        product.count -= cnt 
    
    def withdraw_money(self, client, money_to_withdraw):
        client.money -= money_to_withdraw

    @staticmethod
    def ask(text):
        # пользователь вводит текст
        return input(text)
    
    @staticmethod
    def show(text):
        # отображаем текст пользователю
        print(text)



    def drow_graph(self):
        product_names = []
        stock_values = []

        for prod in self.products:
            product_names.append(prod.name)
            stock_values.append(prod.count)
        
        plt.figure(figsize=(10, 6))
        plt.barh(product_names, stock_values, color='skyblue')
        plt.xlabel('Количество в наличии')
        plt.title('Запасы продуктов в пекарне')
        plt.grid(axis='x')
        plt.ioff()
        plt.show(block=False)

        return plt

from random import randint     

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
    bakery = Bakery(name='Пирожки', employes=[barista, baker, kassir], products=[Bread(f'{i*i}', randint(1, 100), randint(1, 100)) for i in range(1, 40)])

    # НАЧАЛО ВЗАИМОДЕЙСТВИЯ
    name, money = 'Витя', 10000
    client = Client(name=name, money=money)
    #name = input('Введите имя: ')
    #money = int(input('Сколько у вас денег: '))
    
    print(f'ДОБРО ПОЖАЛОВАТЬ В ПЕКАРНЮ {bakery.name}!')
    while True:
        bakery.start(client)

        if input('Вы хотите купить что-то еще? ').lower() in ('нет', 'не'):
            print('Приходите еще!')
            break
