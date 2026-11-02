import pytest
from src.classes import Category, Product, load_data_from_json


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
    assert len(category.products) == 2


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
    assert result[0].products[0].name == "Iphone"
