import matplotlib.pyplot as plt


from products import Bread, Pizza, Product
from employee import Baker, Kassir, Boss, Barista, Employee

from enum import Enum, auto

class State(Enum):
    exists = auto()
    missing = auto()
    not_exists = auto()



class Client:
    def __init__(self, name: str, money: int):
        self.name= name
        self.money = money

class Bakery:
    def __init__(self, name, products=list[Product], employes=list[Employee]):
        self.name = name
        self.products = products
        self.employes = employes

    def start(self, client: Client) -> None:
        """
        метод для запуска пекарни
        """
        plt = self.drow_graph()

        product = self.choose_product()
        cnt = self.choose_count(product=product)
        self.calculate_purchase(product, cnt, client)
        plt.close()


    def calculate_purchase(self, product, cnt, client) -> None:
        """
        Метод для расчета покупки
        """
        summary_price = product.price*int(cnt)

        if self.enough_money(summary_price, client.money):
            self.show(f'Спасибо за покупку. Вы купили {product.name} за {summary_price} руб.')
            self.change_count(product, int(cnt))
            self.withdraw_money(client, summary_price)
        else: 
            self.show(f'У вас не хватает денег. \n Товар стоит: {summary_price} руб., а у вас {client.money} руб.')

    def choose_product(self) -> Product:
        """
        Метод для выбора продукции
        Возвращает Product
        """
        while True:
            product = self.ask('Выберите товар, укажите его название: ')
            state, ans, product = self.product_exists(product=product)
            self.show(ans)
            match state:
                case State.exists:
                    break
                case State.not_exists:
                    boss = self.get_employee(Boss)
                    boss.get_feedback()
                case State.missing:
                    baker = self.get_employee(Baker)
                    baker.bake(product)


        return product
    
    def choose_count(self, product: Product) -> int:
        """
        Метод для выбора кол-ва продукции пользователем
        Возвращает кол-во продукции выбранное пользователем
        """
        while True:
            count = self.ask(f'Выберите кол-во товара (доступно {product.count}): ')
            if self.enough_count(product, count):
                break
            self.show('Извините, но товара не хватает, выберите другое кол-во!')
        return count


    def product_exists(self, product: str):
        """
        Проверка на существование продукта
        Возвращает bool, str, Product
        """
        if any(pos for pos in self.products if pos.name == product):
            product = [prod for prod in self.products if prod.name == product][0]
            if product.count != 0:
                return State.exists, 'Такой товар есть, какое количество вам нужно?', product
            return State.missing, 'Извините, но товар закончился, сейчас мы его приготовим!', product
        return State.not_exists, 'Простите, но такого товара нет, сейчас мы позовем нашего босса', None

    def enough_count(self, product: Product, cnt) -> bool:
        """
        Проверка на доступное кол-во товара
        """  
        if product.count >= int(cnt):
            return True
        return False

    def enough_money(self, product_price, client_money) -> bool:
        """
        Проверка на доступность покупки
        """
        if product_price <= client_money:
            return True
        return False

    def change_count(self, product: Product, cnt) -> None:
        """
        Изменяет кол-во продукции
        """

        product.count -= cnt 
    
    def withdraw_money(self, client, money_to_withdraw) -> None:
        """
        метод для снятия денег с покупателя
        """
        client.money -= money_to_withdraw

    def get_employee(self, employee: Employee) -> Employee:
        return [emp for emp in self.employes if isinstance(emp, employee)][0]

    @staticmethod
    def ask(text) -> input:
        # пользователь вводит текст
        return input(text)
    
    @staticmethod
    def show(text) -> None:
        # отображаем текст пользователю
        print(text)



    def drow_graph(self) -> plt:
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
    production = [
        Bread('1', 0, 1000, 0.5),
        Bread('ч. хлеб', 0, 1000, 0.5),
        Bread('ржаной хлеб', 0, 100000, 0.5),
        Pizza('Пеперони', 0, 10000, 0.5),
        Pizza('Гавайская', 0, 10000, 0.5)
    ]


    # СОЗДАЕМ СОТРУДНИКОВ
    employes = [
        Boss('Кирилл', 1_000_000),
        Baker('Саша', 1_000_001),
        Kassir('Влад', 999_999)
    ]

    # ИНИЦИАЛИЗАЦИЯ ПЕКАРНИ
    bakery = Bakery(name='Пирожки', employes=employes, products=production)

    # НАЧАЛО ВЗАИМОДЕЙСТВИЯ
    name, money = 'Витя', 10000
    client = Client(name=name, money=money)
    #name = input('Введите имя: ')
    #money = int(input('Сколько у вас денег: '))
    
    bakery.show(f'ДОБРО ПОЖАЛОВАТЬ В ПЕКАРНЮ {bakery.name}!')
    while True:
        bakery.start(client)

        if input('Вы хотите купить что-то еще? ').lower() in ('нет', 'не'):
            bakery.show('Приходите еще!')
            break
