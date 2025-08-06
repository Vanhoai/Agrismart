class Employee:
    def __init__(self, name: str, age: int) -> None:
        self.__name = name
        self.__age = age

    @property
    def name(self) -> str:
        return self.__name

    @property
    def age(self) -> int:
        return self.__age


class SellEmployee(Employee):
    def __init__(self, name: str, age: int, products: int) -> None:
        super().__init__(name, age)
        self.__products = products

    @property
    def products(self) -> int:
        return self.__products


def main() -> None:
    sell = SellEmployee("John", 30, 100)

    print(sell.name)
    print(sell.age)
    print(sell.products)
