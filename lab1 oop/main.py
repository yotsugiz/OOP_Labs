#1.1
# Відповідає лише за формування звіту
class CallReportGenerator:
    def generate_report(self):
        print("Звіт сформовано")

# Відповідає лише за збереження
class CallReportRepository:
    def save(self):
        print("Звіт збережено у файл")
#1.2
# Відповідає лише за зберігання даних
class Subscriber:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

# Відповідає лише за відправку SMS
class SMSSender:
    def send_sms(self):
        print("SMS відправлено")

# Відповідає лише за розрахунок балансу
class BalanceCalculator:
    def calculate(self):
        print("Баланс розраховано")

