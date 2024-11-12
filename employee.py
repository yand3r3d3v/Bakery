class Employee:
    def __init__(self, name, income):
        self.name=name
        self.income=income

class Kassir(Employee):
    def __init__(self, name, income):
        super().__init__(name, income)

class Baker(Employee):
    def __init__(self, name, income):
        super().__init__(name, income)

class Boss(Employee):
    def __init__(self, name, income):
        super().__init__(name, income)

class Barista(Employee):
    def __init__(self, name, income):
        super().__init__(name, income)