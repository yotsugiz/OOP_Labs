import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re

class DataProcessor:
    """Клас для завантаження та попередньої обробки даних."""
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        try:
            self.df = pd.read_csv(self.file_path)
            print("Дані успішно завантажено.")
        except FileNotFoundError:
            print(f"Помилка: Файл {self.file_path} не знайдено.")

    def clean_and_prepare_data(self):
        if self.df is None:
            return

        # 1. Створення числової колонки Average Salary
        def calculate_average_salary(salary_str):
            if pd.isna(salary_str):
                return None
            # Витягуємо всі числа з рядка (наприклад, з "$50k - $70k" або "50000-70000")
            numbers = [int(n) for n in re.findall(r'\d+', str(salary_str).replace(',', ''))]
            if len(numbers) == 2:
                # Якщо зарплата вказана в тисячах (наприклад, 50-70), множимо на 1000
                if numbers[0] < 1000:
                    numbers = [n * 1000 for n in numbers]
                return sum(numbers) / 2
            return None

        self.df['Average Salary'] = self.df['Salary Range'].apply(calculate_average_salary)

        # 2. Витягування року публікації (Year) з Date Posted
        self.df['Date Posted'] = pd.to_datetime(self.df['Date Posted'], errors='coerce')
        self.df['Year'] = self.df['Date Posted'].dt.year

        # Видаляємо рядки з порожніми значеннями, які нам критичні для графіків
        self.df.dropna(subset=['Average Salary', 'Year'], inplace=True)
        self.df['Year'] = self.df['Year'].astype(int)

    def get_data(self):
        return self.df

class DataVisualizer:
    """Клас для побудови графіків за допомогою Seaborn."""
    def __init__(self, df):
        self.df = df
        # Налаштування стилю та фірмової контрастної палітри
        sns.set_theme(style="darkgrid")
        self.custom_palette = ['#8A0303', '#39FF14', '#007ACC', '#FF8C00', '#8A2BE2']
        sns.set_palette(self.custom_palette)

    def plot_barplot(self):
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Experience Level', y='Average Salary', data=self.df, errorbar=None, palette=self.custom_palette)
        plt.title('Залежність середньої зарплати від рівня досвіду')
        plt.xlabel('Рівень досвіду')
        plt.ylabel('Середня зарплата ($)')
        plt.show()

    def plot_boxplot(self):
        plt.figure(figsize=(10, 12)) # Робимо полотно вищим, а не ширшим
        # Міняємо змінні місцями: X стає зарплатою, Y стає галуззю
        sns.boxplot(x='Average Salary', y='Industry', data=self.df, color='#8A0303')
        plt.title('Розподіл зарплат за галузями')
        plt.xlabel('Середня зарплата ($)')
        plt.ylabel('Галузь')
        # Поворот тексту тут вже не потрібен
        plt.tight_layout()
        plt.show()

    def plot_heatmap(self):
        plt.figure(figsize=(10, 6))
        # Використовуємо crosstab для підрахунку кількості вакансій
        pivot_table = pd.crosstab(self.df['Experience Level'], self.df['Industry'])
        # Теплова карта в зелених тонах
        custom_cmap = sns.light_palette("#39FF14", as_cmap=True)
        sns.heatmap(pivot_table, annot=True, cmap=custom_cmap, fmt='d', linewidths=0.5)
        plt.title('Кількість вакансій за рівнем досвіду та галуззю')
        plt.xlabel('Галузь')
        plt.ylabel('Рівень досвіду')
        plt.show()

    def plot_scatterplot(self):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='Year', y='Average Salary', hue='Experience Level', data=self.df,
                        palette=self.custom_palette, s=100, alpha=0.8)
        plt.title('Залежність зарплати від року публікації вакансії')
        plt.xlabel('Рік публікації')
        plt.ylabel('Середня зарплата ($)')
        plt.xticks(self.df['Year'].unique()) # Щоб роки відображались цілими числами
        plt.legend(title='Рівень досвіду', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

    def plot_pairplot(self):
        # Відбираємо лише потрібні колонки для парних графіків
        pair_df = self.df[['Average Salary', 'Year', 'Experience Level']].dropna()
        sns.pairplot(pair_df, hue='Experience Level', palette=self.custom_palette, diag_kind='kde')
        plt.suptitle('Парні графіки: Зарплата, Рік та Рівень досвіду', y=1.02)
        plt.show()

# --- Головний блок виконання ---
if __name__ == "__main__":
    # 1. Ініціалізація та обробка даних
    processor = DataProcessor('Job opportunities.csv')
    processor.load_data()
    processor.clean_and_prepare_data()
    df_cleaned = processor.get_data()

    if df_cleaned is not None:
        # 2. Ініціалізація візуалізатора
        visualizer = DataVisualizer(df_cleaned)

        # 3. Виклик методів для побудови графіків
visualizer.plot_barplot()
visualizer.plot_boxplot()
visualizer.plot_heatmap()
visualizer.plot_scatterplot()
visualizer.plot_pairplot()