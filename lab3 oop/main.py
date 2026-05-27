import pandas as pd

# 1. Клас для завантаження та первинного аналізу

class DataLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_data(self):
        # Завантаження датасету
        self.df = pd.read_csv(self.filepath)
        return self.df

    def initial_analysis(self):
        print("--- Первинний аналіз даних ---")
        print("Перші 5 рядків:\n", self.df.head())
        print("\nОстанні 5 рядків:\n", self.df.tail())

        rows, cols = self.df.shape
        print(f"\nКількість рядків: {rows}, Кількість стовпців: {cols}")

        memory_mb = self.df.memory_usage(deep=True).sum() / (1024 ** 2)
        print(f"Обсяг пам’яті: {memory_mb:.2f} MB")

        print("\nТипи даних:\n", self.df.dtypes)
        print("\nПропущені значення:\n", self.df.isnull().sum())


# 2. Клас для фільтрації даних

class DataFilter:
    def __init__(self, df):
        self.df = df

    def filter_by_industry(self, industry_name="Cloud Computing"):
        return self.df[self.df['Industry'] == industry_name]

    def filter_senior_level(self):
        # Припускаємо, що рівень вказаний у назві посади (Job Title) або окремому стовпці
        return self.df[self.df['Job Title'].str.contains("Senior", case=False, na=False)]

    def filter_type_and_city(self, job_type="Full-Time", city="New York"):
        # Припускаємо наявність стовпців 'Job Type' та 'Location'
        return self.df[(self.df['Job Type'] == job_type) & (self.df['Location'] == city)]


# 3. Клас для обробки та сортування зарплат

class DataSorter:
    def __init__(self, df):
        self.df = df.copy()

    def clean_salary_data(self):
        # Витягуємо мінімальну та максимальну зарплату з тексту (наприклад, "$50,000 - $80,000")
        # Створюємо два нових числових стовпці
        extracted = self.df['Salary Range'].str.extract(r'\$?(\d+,?\d*)\s*-\s*\$?(\d+,?\d*)')
        self.df['Min Salary'] = extracted[0].str.replace(',', '').astype(float)
        self.df['Max Salary'] = extracted[1].str.replace(',', '').astype(float)
        return self.df

    def sort_by_salary_and_get_top(self):
        sorted_df = self.df.sort_values(by='Max Salary', ascending=False)
        print("\n--- 5 вакансій з найвищою зарплатою ---")
        print(sorted_df[['Job Title', 'Salary Range', 'Max Salary']].head(5))
        return sorted_df


# 4. Клас для групування та створення нових ознак

class DataAnalyzer:
    def __init__(self, df):
        self.df = df.copy()

    def group_by_industry(self):
        print("\n--- Аналіз за галузями (Industry) ---")
        stats = self.df.groupby('Industry').agg(
            vacancies_count=('Job Title', 'count'),
            avg_min_salary=('Min Salary', 'mean')
        )
        print(stats)

        top_industry = stats.sort_values(by='avg_min_salary', ascending=False).index[0]
        print(f"\nГалузь з найвищою середньою зарплатою: {top_industry}")

    def categorize_salary(self):
        def get_category(max_sal):
            if pd.isna(max_sal): return 'Unknown'
            if max_sal <= 40000:
                return 'Low'
            elif 40001 <= max_sal <= 70000:
                return 'Medium'
            else:
                return 'High'

        self.df['Salary Category'] = self.df['Max Salary'].apply(get_category)
        print("\n--- Перевірка категоризації зарплат ---")
        print(self.df[['Max Salary', 'Salary Category']].head())
        return self.df

    def time_analysis(self):
        # Перетворення у datetime та створення колонки Year
        self.df['Date Posted'] = pd.to_datetime(self.df['Date Posted'])
        self.df['Year'] = self.df['Date Posted'].dt.year

        print("\n--- Кількість вакансій за роками ---")
        yearly_stats = self.df.groupby('Year').agg(
            vacancies_count=('Job Title', 'count')
        )
        print(yearly_stats)

        most_active_year = yearly_stats.sort_values(by='vacancies_count', ascending=False).index[0]
        print(f"Найбільш активний рік: {most_active_year}")


# ГОЛОВНИЙ БЛОК ВИКОНАННЯ

if __name__ == "__main__":
    # 1. Ініціалізація та завантаження (вставте правильний шлях до файлу!)
    loader = DataLoader('Job opportunities.csv')
    df = loader.load_data()
    loader.initial_analysis()

    # 2. Фільтрація (демонстрація роботи методів)
    filter_engine = DataFilter(df)
    cloud_jobs = filter_engine.filter_by_industry("Cloud Computing")
    senior_jobs = filter_engine.filter_senior_level()

    # 3. Сортування та очищення зарплат (трансформація тексту в числа)
    sorter = DataSorter(df)
    df_with_salaries = sorter.clean_salary_data()
    sorter.sort_by_salary_and_get_top()

    # 4. Аналітика, застосування apply() та часовий аналіз
    analyzer = DataAnalyzer(df_with_salaries)
    analyzer.group_by_industry()
    df_final = analyzer.categorize_salary()
    analyzer.time_analysis()