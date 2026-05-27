import asyncio
import websockets
from websockets.exceptions import ConnectionClosed, InvalidURI


class WebSocketClient:
    def __init__(self):
        self.websocket = None

    async def connect(self, url):
        """Встановлює WebSocket-з'єднання за вказаною адресою."""
        try:
            self.websocket = await websockets.connect(url)
            print(f"[УСПІХ] З'єднання з {url} встановлено.")
        except InvalidURI:
            print("[ПОМИЛКА] Неправильний формат URL-адреси.")
        except Exception as e:
            print(f"[ПОМИЛКА ПІДКЛЮЧЕННЯ] Сервер не відповідає або сталася помилка: {e}")

    async def send_message(self, message):
        """Надсилає повідомлення серверу."""
        # Залишаємо лише перевірку на те, чи існує об'єкт websocket
        if self.websocket:
            try:
                await self.websocket.send(message)
                print(f"[КЛІЄНТ -> СЕРВЕР]: {message}")
            except ConnectionClosed:
                print("[ПОМИЛКА] З'єднання було перервано під час відправки.")
            except Exception as e:
                print(f"[ПОМИЛКА] Не вдалося надіслати повідомлення: {e}")
        else:
            print("[УВАГА] Неможливо надіслати повідомлення, з'єднання не встановлено.")

    async def receive_message(self):
        """Отримує повідомлення від сервера."""
        # Залишаємо лише перевірку на те, чи існує об'єкт websocket
        if self.websocket:
            try:
                message = await self.websocket.recv()
                print(f"[СЕРВЕР -> КЛІЄНТ]: {message}")
                return message
            except ConnectionClosed:
                print("[ПОМИЛКА] З'єднання було закрито сервером.")
            except Exception as e:
                print(f"[ПОМИЛКА] Під час отримання даних сталася помилка: {e}")
        else:
            print("[УВАГА] Неможливо отримати повідомлення, з'єднання не встановлено.")
        return None

    async def close_connection(self):
        """Закриває WebSocket-з'єднання."""
        if self.websocket:
            await self.websocket.close()
            print("[СТАТУС] З'єднання безпечно закрито.")


# --- Демонстрація роботи клієнта ---
async def main():
    # Використовуємо один із доступних тестових серверів
    test_url = "wss://ws.postman-echo.com/raw"
    client = WebSocketClient()

    print("--- Початок тестування WebSocketClient ---")

    # 1. Підключення
    await client.connect(test_url)

    # 2. Відправка повідомлень та отримання відповідей
    # (Передаємо дані відповідно до 5 варіанту)
    test_messages = [
        "Привіт, сервер! Це тестове повідомлення.",
        "Запит даних для варіанту 5."
    ]

    for msg in test_messages:
        await client.send_message(msg)
        # Сервер echo просто повертає відправлене повідомлення назад
        await client.receive_message()
        await asyncio.sleep(1)  # Невелика пауза між повідомленнями

    # 3. Демонстрація обробки помилок (спроба відправити на закрите з'єднання)
    print("\n--- Демонстрація закриття та обробки помилок ---")
    await client.close_connection()
    await client.send_message("Це повідомлення не має відправитись.")


if __name__ == "__main__":
    # Запуск асинхронного циклу подій
    asyncio.run(main())