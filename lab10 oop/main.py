import unittest
from unittest.mock import Mock
from parameterized import parameterized


# ЗАВДАННЯ 1: Клас MathToo;

class MathTool:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Ділення на нуль неможливе!")
        return a / b

# ЗАВДАННЯ 2: Клас LibraryItem

class LibraryItem:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def details(self):
        return f"Книга: '{self.title}', Автор: {self.author}, Рік видання: {self.year}"

# ЗАВДАННЯ 3: Взаємодія класів

class NotificationService:
    def send(self, message, user):
        # Імітація реальної відправки повідомлення (наприклад, SMS або Email)
        pass


class UserManager:
    def __init__(self, service):
        self.service = service

    def notify_user(self, user, message):
        self.service.send(message, user)

# ЗАВДАННЯ 4: Функція перевірки парності

def check_even(number):
    return number % 2 == 0

# БЛОК ЮНІТ-ТЕСТІВ

class TestOOPLaboratory(unittest.TestCase):

    # --- Тести для завдання 1 (MathTool) ---
    def setUp(self):
        """Виконується перед кожним тестом, створюючи свіжий екземпляр класу"""
        self.math_tool = MathTool()

    def test_add(self):
        self.assertEqual(self.math_tool.add(5, 10), 15)

    def test_subtract(self):
        self.assertEqual(self.math_tool.subtract(10, 5), 5)

    def test_multiply(self):
        self.assertEqual(self.math_tool.multiply(5, 4), 20)

    def test_divide_normal(self):
        self.assertEqual(self.math_tool.divide(20, 5), 4)

    def test_divide_by_zero(self):
        # Перевірка, що при діленні на 0 викидається ValueError
        with self.assertRaises(ValueError):
            self.math_tool.divide(5, 0)

    # --- Тести для завдання 2 (LibraryItem) ---
    def test_library_item_details(self):
        book = LibraryItem("Об'єктно-орієнтоване програмування", "Джон Сміт", 2023)
        expected_string = "Книга: 'Об'єктно-орієнтоване програмування', Автор: Джон Сміт, Рік видання: 2023"
        self.assertEqual(book.details(), expected_string)

    # --- Тести для завдання 3 (Mock-об'єкти) ---
    def test_notify_user(self):
        # Створюємо мок-об'єкт замість реального сервісу
        mock_service = Mock(spec=NotificationService)
        user_manager = UserManager(mock_service)

        # Викликаємо метод, який хочемо протестувати
        user_manager.notify_user("student_ix21", "Лабораторна здана!")

        # Перевіряємо, чи метод send був викликаний з правильними параметрами
        mock_service.send.assert_called_once_with("Лабораторна здана!", "student_ix21")

    # --- Тести для завдання 4 (Параметризовані тести) ---
    @parameterized.expand([
        ("positive_even", 4, True),
        ("positive_odd", 5, False),
        ("zero", 0, True),
        ("negative_even", -8, True),
        ("negative_odd", -3, False),
    ])
    def test_check_even(self, name, val, expected):
        # name - просто опис тесту для зручності читання логів
        self.assertEqual(check_even(val), expected)


# Запуск всіх тестів
if __name__ == '__main__':
    unittest.main()