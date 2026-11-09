import json


class Product:
    """Класс для представления товара."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self) -> str:
        """Строковое отображение продукта с приватным атрибутом."""
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """Сложение продуктов с использованием приватных атрибутов."""
        return (
            (self.__price * self.quantity) + (other.__price * other.quantity)
        )

    @classmethod
    def new_product(
        cls, product_data: dict, current_products: list | None = None
    ) -> "Product":
        """Создает продукт из словаря (с проверкой дубликатов)."""
        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        if current_products:
            for existing_product in current_products:
                if existing_product.name == name:
                    existing_product.quantity += quantity
                    if price > existing_product.price:
                        existing_product.price = price
                    return existing_product

        return cls(name, description, price, quantity)

    @property
    def price(self) -> float:
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверками и подтверждением снижения."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            user_choice = input(
                f"Вы уверены, что хотите снизить цену с {self.__price} "
                f"до {new_price}? (y/n): "
            )
            if user_choice.lower() != "y":
                print("Снижение цены отменено")
                return

        self.__price = new_price


class Category:
    """Класс для представления категории товаров."""

    category_count = 0
    product_count = 0

    def __init__(
        self, name: str, description: str, products: list | None = None
    ) -> None:
        self.name = name
        self.description = description
        self.__products = []

        Category.category_count += 1

        if products:
            for product in products:
                self.add_product(product)

    def __str__(self) -> str:
        """Строковое отображение категории."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в категорию."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер возвращает список товаров."""
        result = ""
        for product in self.__products:
            result += f"{str(product)}\n"
        return result

    @property
    def products_list(self) -> list[Product]:
        """Возвращает приватный список объектов продуктов."""
        return self.__products


class CategoryIter:
    """Вспомогательный класс-итератор."""

    def __init__(self, category: Category) -> None:
        self.products = category.products_list
        self.index = 0

    def __iter__(self) -> "CategoryIter":
        self.index = 0
        return self

    def __next__(self) -> Product:
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        else:
            raise StopIteration


def load_data_from_json(file_path: str) -> list[Category]:
    """Загрузка данных из файла JSON и создание объектов."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []

    categories = []
    for cat_data in data:
        products_list = []
        for prod_data in cat_data.get("products", []):
            product = Product(
                name=prod_data["name"],
                description=prod_data["description"],
                price=prod_data["price"],
                quantity=prod_data["quantity"],
            )
            products_list.append(product)

        category = Category(
            name=cat_data["name"],
            description=cat_data["description"],
            products=products_list,
        )
        categories.append(category)

    return categories
