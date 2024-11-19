import matplotlib.pyplot as plt

from products import Bread, Pizza, Product, Coffee, Dessert
from employee import Baker, Kassir, Boss, Barista, Employee

from enum import Enum, auto

class State(Enum):
    exists = auto()
    missing = auto()
    not_exists = auto()

class Purchase:
    pass

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

        if self.enough_money(summary_price, client):
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
            kassir = self.get_employee(Kassir)
            boss = self.get_employee(Boss)
            baker = self.get_employee(Baker)
            barista = self.get_employee(Barista)
            product = self.ask('Выберите товар, укажите его название: ')
            state, ans, product = self.product_exists(product=product)
            self.show(ans, employee=kassir)
            match state:
                case State.exists:
                    break
                case State.not_exists:
                    boss.get_feedback()
                case State.missing:
                    if self.enough_money(100, client):
                        coffee = self.ask('Пока мы готовим, вы хотите кофе? ', employee=barista)
                        if coffee.lower() == 'да':
                            self.show('СПИСОК ДОСТУПНОГО КОФЕ:')
                            for prod in self.get_category_product(Coffee):
                                self.show(f'{prod.name} {prod.price} руб.')
                            selected_coffee = self.choose_product()
                            selected_cnt = self.choose_count(selected_coffee)
                            self.calculate_purchase(selected_coffee, selected_cnt, client)
                            #self.show(employee=barista, text='Вот ваш кофе. С вас 100$')
                    baker.bake(product)



        return product
    
    def get_category_product(self, product_type: Product) -> list[Product]:
        products = []
        for prod in self.products:
            if isinstance(prod, product_type):
                products.append(prod)
        return products

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
        try:
            product = [prod for prod in self.products if prod.name == product][0]
        except:
            product = None
        if product:
            if product.count != 0:
                return State.exists, 'Такой товар есть, какое количество вам нужно?', product
            return State.missing, 'Извините, но товар закончился, сейчас мы его приготовим!', product
        return State.not_exists, 'Простите, но такого товара нет, сейчас мы позовем нашего босса', product

    def enough_count(self, product: Product, cnt) -> bool:
        """
        Проверка на доступное кол-во товара
        """  
        if product.count >= int(cnt):
            return True
        return False

    def enough_money(self, product_price, client: Client) -> bool:
        """
        Проверка на доступность покупки
        """
        if product_price <= client.money:
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
    def ask(text, employee = None) -> str:
        # пользователь вводит текст
        if employee == None:
            return input(text)
        return input(f'{employee.info()}: {text}')
    
    @staticmethod
    def show(text, employee = None) -> None:
        # отображаем текст пользователю
        if employee == None: 
            print(text)
            return
        print(f'{employee.info()} {text}')



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

if __name__ == '__main__':
    # СОЗДАЕМ ПРОДУКЦИЮ
    production = [
        Bread('черный хлеб', 0, 1000, 2),
        Bread('ржаной хлеб', 0, 1000, 2),
        Bread('белый хлеб', 0, 1000, 2),
        
        Pizza('Пеперони', 0, 100, 3),
        Pizza('Гавайская', 0, 100, 3),
        Pizza('Мясная', 0, 100, 3),
        Pizza('Четыре сыра', 0, 100, 3),
        
        Dessert('Медовик', 0, 50, 4),
        Dessert('Наполеон', 0, 50, 4),
        Dessert('Чизкейк', 0, 80, 4),
        Dessert('Торт бисквитный', 0, 50, 4),
        Dessert('Безе', 0, 150, 4),
        Dessert('Эклер', 0, 150, 4),
        Dessert('Тирамису', 0, 76, 4),
        
        Coffee('Американо', 1, 1, 1),
        Coffee('Капучино', 1, 1, 1)
    ]


    # СОЗДАЕМ СОТРУДНИКОВ
    employes = [
        Boss('Кирилл', 1_000_000),
        Baker('Саша', 1_000_001),
        Kassir('Влад', 999_999),
        Barista('Вадим', 10_000)
    ]

    # ИНИЦИАЛИЗАЦИЯ ПЕКАРНИ
    bakery = Bakery(name='Пирожки', employes=employes, products=production)

    # НАЧАЛО ВЗАИМОДЕЙСТВИЯ
    name, money = 'Витя', 0
    client = Client(name=name, money=money)
    #name = input('Введите имя: ')
    #money = int(input('Сколько у вас денег: '))
    
    bakery.show(f'ДОБРО ПОЖАЛОВАТЬ В ПЕКАРНЮ {bakery.name}!')
    while True:
        bakery.start(client)

        if input('Вы хотите купить что-то еще? ').lower() in ('нет', 'не'):
            bakery.show('Приходите еще!')
            break
