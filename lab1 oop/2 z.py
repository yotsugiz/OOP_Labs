from abc import ABC, abstractmethod

class Tariff(ABC):
    @abstractmethod
    def calculate_cost(self, usage):
        pass

class VoiceTariff(Tariff):
    def calculate_cost(self, minutes):
        return minutes * 1.0

class DataTariff(Tariff):
    def calculate_cost(self, megabytes):
        return megabytes * 0.5

class RoamingTariff(Tariff):
    def calculate_cost(self, minutes):
        return minutes * 5.0

class Connection(ABC):
    @abstractmethod
    def establish(self):
        pass

class NetworkConnection(Connection):
    @abstractmethod
    def establish(self):
        pass

class WiFiConnection(NetworkConnection):
    def establish(self):
        print("Підключено через WiFi")

class LTEConnection(NetworkConnection):
    def establish(self):
        print("Підключено через LTE")

# Виправлення для супутника: він є Connection, але не звичайним NetworkConnection
class SatelliteConnection(Connection):
    def establish(self):
        print("Встановлення супутникового з'єднання (з урахуванням затримок)")

class ICallable(ABC):
    @abstractmethod
    def make_call(self): pass

class IMessageable(ABC):
    @abstractmethod
    def send_sms(self): pass

class INetworkConnectable(ABC):
    @abstractmethod
    def connect_to_network(self): pass

class Smartphone(ICallable, IMessageable, INetworkConnectable):
    def make_call(self): print("Дзвінок")
    def send_sms(self): print("SMS")
    def connect_to_network(self): print("Інтернет")

class IoTDevice(INetworkConnectable):
    def connect_to_network(self):
        print("Передача даних датчика в мережу")


class Logger(ABC):
    @abstractmethod
    def log(self, message): pass

class FileLogger(Logger):
    def log(self, message): print(f"Файл: {message}")

class ServerLogger(Logger):
    def log(self, message): print(f"Сервер: {message}")

class ConsoleLogger(Logger):
    def log(self, message): print(f"Консоль: {message}")

class NetworkMonitor:
    def __init__(self, logger: Logger):
        self.logger = logger  # Залежність від абстракції

    def check(self):
        self.logger.log("Мережа працює стабільно")