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