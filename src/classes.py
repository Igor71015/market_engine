import json


class Product:
    """Класс для представления товара."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс для представления категории товаров."""

    # Атрибуты класса для подсчета общего количества
    category_count = 0
    product_count = 0

    def __init__(
        self, name: str, description: str, products: list | None = None
    ) -> None:
        self.name = name
        self.description = description
        self.products = products if products is not None else []

        # Автоматический подсчет при создании нового объекта категории
        Category.category_count += 1
        # Подсчитываем количество уникальных товаров в этой категории
        Category.product_count += len(self.products)


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
