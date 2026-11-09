import pytest
from src.classes import Category, CategoryIter, Product, load_data_from_json


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Фикстура для сброса счетчиков перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_products():
    """Фикстура для создания тестовых продуктов."""
    p1 = Product("Samsung Galaxy S23 Ultra", "256GB, Gray", 120000.0, 5)
    p2 = Product("Iphone 15 Pro", "512GB, Gray", 150000.0, 10)
    return [p1, p2]


def test_product_initialization():
    """Тест корректности инициализации объекта Product."""
    product = Product("Телевизор", "4K Smart TV", 50000.0, 3)
    assert product.name == "Телевизор"
    assert product.description == "4K Smart TV"
    assert product.price == 50000.0
    assert product.quantity == 3


def test_category_initialization(sample_products):
    """Тест корректности инициализации объекта Category."""
    category = Category("Электроника", "Гаджеты и техника", sample_products)
    assert category.name == "Электроника"
    assert category.description == "Гаджеты и техника"
    assert "Samsung Galaxy S23 Ultra" in category.products


def test_category_counters(sample_products):
    """Тест подсчета количества категорий и уникальных продуктов."""
    assert Category.category_count == 0
    assert Category.product_count == 0

    Category("Электроника", "Гаджеты", sample_products)
    assert Category.category_count == 1
    assert Category.product_count == 2


def test_load_data_from_json(tmp_path):
    """Тест: полная загрузка корректного JSON-файла."""
    assert load_data_from_json("non_existent_file.json") == []

    test_file = tmp_path / "test_products.json"
    raw_json = (
        '[{"name": "Смартфоны", "description": "Гаджеты", "products": ['
        '{"name": "Iphone", "description": "128GB", '
        '"price": 1000.0, "quantity": 5}'
        ']}]'
    )
    test_file.write_text(raw_json, encoding="utf-8")

    result = load_data_from_json(str(test_file))
    assert len(result) == 1
    assert result[0].name == "Смартфоны"


def test_price_setter_invalid(capsys):
    """Тест попытки установить некорректную цену."""
    product = Product("Телевизор", "4K Smart TV", 50000.0, 3)
    product.price = -100
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 50000.0


def test_price_setter_decrease_confirm(monkeypatch):
    """Тест подтверждения снижения цены."""
    product = Product("Телевизор", "4K Smart TV", 50000.0, 3)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    product.price = 45000.0
    assert product.price == 45000.0


def test_price_setter_decrease_cancel(monkeypatch, capsys):
    """Тест отмены снижения цены."""
    product = Product("Телевизор", "4K Smart TV", 50000.0, 3)
    monkeypatch.setattr("builtins.input", lambda _: "n")
    product.price = 45000.0
    captured = capsys.readouterr()
    assert "Снижение цены отменено" in captured.out
    assert product.price == 50000.0


def test_new_product_duplicate():
    """Тест создания продукта с обработкой дубликатов."""
    p1 = Product("Iphone", "128GB", 1000.0, 5)
    data = {
        "name": "Iphone", "description": "256GB",
        "price": 1200.0, "quantity": 3
    }

    updated_product = Product.new_product(data, [p1])
    assert updated_product.quantity == 8
    assert updated_product.price == 1200.0


def test_product_str():
    """Тест магического метода __str__ класса Product."""
    product = Product("Телевизор", "4K Smart TV", 50000.0, 3)
    assert str(product) == "Телевизор, 50000.0 руб. Остаток: 3 шт."


def test_category_str(sample_products):
    """Тест магического метода __str__ класса Category."""
    category = Category("Электроника", "Гаджеты", sample_products)
    assert str(category) == "Электроника, количество продуктов: 15 шт."


def test_product_add():
    """Тест магического метода __add__ класса Product."""
    p1 = Product("Товар A", "Описание", 100.0, 10)
    p2 = Product("Товар B", "Описание", 200.0, 2)
    assert p1 + p2 == 1400.0


def test_category_iterator(sample_products):
    """Тест итератора для обхода товаров категории."""
    category = Category("Электроника", "Гаджеты", sample_products)
    iterator = CategoryIter(category)

    products_iterated = []
    for product in iterator:
        products_iterated.append(product)

    assert len(products_iterated) == 2
    assert products_iterated[0].name == "Samsung Galaxy S23 Ultra"
