from time import sleep

class Employee:
    JOB = 'Работник'
    def __init__(self, name, income):
        self.name=name
        self.income=income

    @classmethod
    def info(cls):
        return f'{cls.JOB}:'

class Kassir(Employee):
    JOB = 'Кассир'

class Baker(Employee):
    JOB = 'Пекарь'
    def __init__(self, name, income, performance=10):
        super().__init__(name, income)
        self.performance = performance

    def bake(self, product):
        sleep(product.time)

        product.count += self.performance

        print(f'{self.info()} Товар {product.name} приготовлен в кол-ве {self.performance} шт.') 

class Boss(Employee):
    JOB = 'Босс'
    
    def get_feedback(self):
        print(f'{self.info()} Здравствуйте, спасибо за ваше предложение, мы его обязательно рассмотрим.')

class Barista(Employee):
    JOB = 'Бариста'