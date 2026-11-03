import json


class Product:
    """Класс для представления товара."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут цены
        self.quantity = quantity

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
        self.__products = []  # Приватный атрибут списка товаров

        Category.category_count += 1

        if products:
            for product in products:
                self.add_product(product)

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в категорию и обновляет счетчик товаров."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер возвращает список товаров в виде отформатированных строк."""
        result = ""
        for product in self.__products:
            result += (
                f"{product.name}, {product.price} руб. "
                f"Остаток: {product.quantity} шт.\n"
            )
        return result


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
