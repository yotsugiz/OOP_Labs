import requests
import asyncio
import websockets
import paho.mqtt.client as mqtt
import time
from websockets.exceptions import ConnectionClosed

# 1. Клас для роботи з REST API

class RestClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[REST ПОМИЛКА] Не вдалося отримати дані: {e}")
            return None
# 2. Клас для роботи з WebSocket

class WebSocketClient:
    def __init__(self):
        self.websocket = None

    async def connect(self, url):
        try:
            self.websocket = await websockets.connect(url)
            print(f"[WS УСПІХ] З'єднання з {url} встановлено.")
        except Exception as e:
            print(f"[WS ПОМИЛКА ПІДКЛЮЧЕННЯ]: {e}")

    async def send_message(self, message):
        if self.websocket:
            try:
                await self.websocket.send(message)
                print(f"[WS КЛІЄНТ -> СЕРВЕР]: {message}")
            except Exception as e:
                print(f"[WS ПОМИЛКА] Відправка: {e}")

    async def receive_message(self):
        if self.websocket:
            try:
                message = await self.websocket.recv()
                print(f"[WS СЕРВЕР -> КЛІЄНТ]: {message}")
                return message
            except Exception as e:
                print(f"[WS ПОМИЛКА] Отримання: {e}")
        return None

    async def close_connection(self):
        if self.websocket:
            await self.websocket.close()
            print("[WS СТАТУС] З'єднання закрито.")


# 3. Клас для роботи з MQTT

class CustomMQTTClient:
    def __init__(self, broker_address, broker_port=1883):
        self.broker_address = broker_address
        self.broker_port = broker_port
        # Використовуємо callback_api_version, як вимагає нова версія paho-mqtt
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        # Прив'язуємо callback-функції
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("[MQTT] Підключено до брокера успішно.")
        else:
            print(f"[MQTT ПОМИЛКА] Код підключення: {reason_code}")

    def on_publish(self, client, userdata, mid, reason_code, properties):
        print(f"[MQTT] Повідомлення успішно опубліковано (mid={mid})")

    def on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        print("[MQTT] Відключено від брокера.")

    def connect(self):
        print(f"[MQTT] Спроба підключення до {self.broker_address}...")
        self.client.connect(self.broker_address, self.broker_port, keepalive=60)
        self.client.loop_start()
        time.sleep(1)  # Даємо час на встановлення з'єднання

    def publish(self, topic, message):
        print(f"[MQTT] Публікація в '{topic}': {message}")
        result = self.client.publish(topic, message, qos=0, retain=False)
        result.wait_for_publish()

    def disconnect(self):
        time.sleep(1)
        self.client.disconnect()
        self.client.loop_stop()

# 4. Інтеграція всієї системи

async def main():
    print("=== ЕТАП 1: Отримання даних через REST API ===")
    rest_api = RestClient("https://jsonplaceholder.typicode.com")
    # Отримуємо дані 5-го варіанту (пост з ID = 5)
    post_data = rest_api.get("/posts/5")

    if not post_data:
        print("Помилка отримання даних. Роботу припинено.")
        return

    # Формуємо рядок для передачі
    data_to_transmit = f"Варіант 5: {post_data['title']}"
    print(f"Отримані дані: {data_to_transmit}\n")

    print("=== ЕТАП 2: Передача даних через WebSocket ===")
    ws_client = WebSocketClient()
    await ws_client.connect("wss://ws.postman-echo.com/raw")

    # Відправляємо отримані дані
    await ws_client.send_message(data_to_transmit)

    # Отримуємо відповідь-відлуння від сервера
    ws_response = await ws_client.receive_message()
    await ws_client.close_connection()
    print("\n")

    print("=== ЕТАП 3: Публікація даних через MQTT ===")
    # Використовуємо публічний тестовий брокер HiveMQ
    mqtt_broker = "broker.hivemq.com"
    mqtt_topic = "telecom/group_ix21/variant_5"

    mqtt_client = CustomMQTTClient(mqtt_broker)
    mqtt_client.connect()

    # Публікуємо дані, які повернув нам WebSocket
    if ws_response:
        mqtt_client.publish(mqtt_topic, ws_response)
    else:
        mqtt_client.publish(mqtt_topic, data_to_transmit)

    mqtt_client.disconnect()
    print("\n=== Всі операції успішно завершено ===")


if __name__ == "__main__":
    asyncio.run(main())
