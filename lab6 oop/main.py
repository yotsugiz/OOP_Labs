import requests

class RestClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint):
        """Виконує HTTP GET-запит та повертає отримані дані."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url)
            # Перевірка статус-коду; якщо помилка (4xx або 5xx), генерується виняток
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as errh:
            print(f"[Помилка HTTP] {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"[Помилка з'єднання] {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"[Помилка часу очікування] {errt}")
        except requests.exceptions.RequestException as err:
            print(f"[Невідома помилка запиту] {err}")
        return None

    def post(self, endpoint, data):
        """Виконує HTTP POST-запит з переданими даними."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            print(f"[Помилка POST-запиту] {err}")
            return None

# --- Демонстрація роботи клієнта ---
if __name__ == "__main__":
    # Базова URL-адреса безкоштовного тестового API
    api = RestClient("https://jsonplaceholder.typicode.com")

    print("=== Демонстрація GET-запиту ===")
    # Отримуємо дані для варіанту 5
    print("Запит даних поста з ID = 5...")
    post_5 = api.get("/posts/5")
    if post_5:
        print(f"Успішно отримано: {post_5}")

    print("\n=== Демонстрація POST-запиту ===")
    print("Створення нового запису...")
    new_data = {
        "title": "Лабораторна робота з ООП",
        "body": "Тестування POST запиту",
        "userId": 21
    }
    created_post = api.post("/posts", new_data)
    if created_post:
        print(f"Успішно створено: {created_post}")

    print("\n=== Демонстрація обробки помилок ===")
    print("Спроба звернутися до неіснуючої кінцевої точки (endpoint)...")
    error_test = api.get("/invalid_endpoint_for_test")