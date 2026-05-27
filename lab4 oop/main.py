import sqlite3
import pandas as pd

# Клас 1: Керування базою даних та підготовка даних (Завдання 1)
class DatabaseManager:
    def __init__(self, db_name, csv_path):
        self.db_name = db_name
        self.csv_path = csv_path
        self.conn = sqlite3.connect(self.db_name)
        self.df = pd.read_csv(self.csv_path)

    def prepare_and_load_data(self):
        # Очищення колонки з зарплатами перед завантаженням в SQL
        extracted = self.df['Salary Range'].str.extract(r'\$?(\d+,?\d*)\s*-\s*\$?(\d+,?\d*)')
        self.df['Min Salary'] = extracted[0].str.replace(',', '').astype(float)
        self.df['Max Salary'] = extracted[1].str.replace(',', '').astype(float)

        # Обчислення середньої зарплати для зручності
        self.df['Avg Salary'] = (self.df['Min Salary'] + self.df['Max Salary']) / 2

        # Конвертація дати у формат datetime
        self.df['Date Posted'] = pd.to_datetime(self.df['Date Posted'])
        self.df['Year'] = self.df['Date Posted'].dt.year

        # Завантаження в SQLite
        self.df.to_sql('jobs', self.conn, if_exists='replace', index=False)
        print("Дані успішно завантажено в таблицю 'jobs'.")

    def close_connection(self):
        self.conn.close()
        print("\nЗ'єднання з базою даних закрито.")

# Клас 2: Основні SQL запити (Завдання 2)
class BasicQueries:
    def __init__(self, connection):
        self.conn = connection

    def execute_query(self, query, description):
        print(f"\n--- {description} ---")
        result = pd.read_sql(query, self.conn)
        print(result)

    def run_basic_tasks(self):
        self.execute_query("SELECT * FROM jobs LIMIT 10;", "Перші 10 вакансій")

        self.execute_query("SELECT * FROM jobs WHERE `Required Skills` LIKE '%SQL%';",
                           "Вакансії з вимогою SQL")

        self.execute_query("SELECT DISTINCT Location, Company FROM jobs;",
                           "Унікальні Location та Company")

# Клас 3: Аналітичні та складні запити (Завдання 3, 4, 5, 6)
class AnalyticsQueries:
    def __init__(self, connection):
        self.conn = connection

    def execute_query(self, query, description):
        print(f"\n--- {description} ---")
        result = pd.read_sql(query, self.conn)
        print(result)

    def run_analytics_tasks(self):
        # Завдання 3
        self.execute_query(
            "SELECT `Experience Level`, AVG(`Avg Salary`) as Average_Salary FROM jobs GROUP BY `Experience Level`;",
            "Середня зарплата для кожного рівня досвіду")

        self.execute_query(
            "SELECT `Experience Level`, COUNT(*) as Vacancies_Count FROM jobs GROUP BY `Experience Level`;",
            "Кількість вакансій для кожного рівня досвіду")

        self.execute_query("SELECT MIN(`Min Salary`) as Absolute_Min, MAX(`Max Salary`) as Absolute_Max FROM jobs;",
                           "Мінімальна та максимальна зарплата серед усіх вакансій")

        # Завдання 4
        self.execute_query(
            "SELECT Industry, COUNT(*) as Jobs_Above_50k FROM jobs WHERE `Min Salary` > 50000 GROUP BY Industry;",
            "Вакансії > £50,000 по індустріях")

        self.execute_query("SELECT Industry, AVG(`Avg Salary`) as Avg_Ind_Salary FROM jobs GROUP BY Industry;",
                           "Середня зарплата для кожної індустрії")

        # Завдання 5
        self.execute_query(
            "SELECT Location, `Experience Level`, COUNT(*) as Vacancy_Count FROM jobs GROUP BY Location, `Experience Level`;",
            "Вакансії за містом та рівнем досвіду")

        self.execute_query(
            "SELECT Industry, `Job Type`, COUNT(*) as Total_Jobs FROM jobs GROUP BY Industry, `Job Type`;",
            "Кількість вакансій за індустрією та типом роботи")

        self.execute_query(
            "SELECT Location, `Experience Level`, AVG(`Avg Salary`) as Avg_Salary FROM jobs GROUP BY Location, `Experience Level`;",
            "Середня зарплата за містом та рівнем досвіду")

        # Завдання 6 (Додаткове)
        self.execute_query("SELECT `Job Title`, `Max Salary`, Company FROM jobs ORDER BY `Max Salary` DESC LIMIT 5;",
                           "5 вакансій з найвищою верхньою межею зарплати")

        self.execute_query(
            "SELECT Company, COUNT(*) as Jobs_in_2023 FROM jobs WHERE Year = 2023 GROUP BY Company ORDER BY Jobs_in_2023 DESC LIMIT 5;",
            "Компанії з найбільшою кількістю вакансій у 2023 році")

# ГОЛОВНИЙ БЛОК ВИКОНАННЯ
if __name__ == "__main__":
    db_manager = DatabaseManager('job_market.db', 'Job opportunities.csv')
    db_manager.prepare_and_load_data()

    basic_queries = BasicQueries(db_manager.conn)
    basic_queries.run_basic_tasks()

    analytics_queries = AnalyticsQueries(db_manager.conn)
    analytics_queries.run_analytics_tasks()

    # Завдання 7
    db_manager.close_connection()