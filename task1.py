import sys

import pandas as pd

INPUT_FILE = "exports_extended.csv"
ANALYSIS_FILE = "analysis_result.csv"
GROUPED_FILE = "grouped_result.csv"
CSV_SEPARATOR = ";"

EXPORTS = "Exports of goods and services (% of GDP)"
GDP = "GDP per capita (current US$)"
POPULATION = "Population, total"

# Поріг для фільтрації: країни, де експорт перевищує 50% ВВП
EXPORTS_THRESHOLD = 50

# Орієнтовні межі груп країн за ВВП на душу населення (US$)
GDP_BINS = [0, 1150, 4500, 14000, float("inf")]
GDP_LABELS = ["Low", "Lower-middle", "Upper-middle", "High"]

# Щоб таблиці виводилися повністю, а не з трикрапками
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

# Завантаження даних із CSV-файлу
try:
    df = pd.read_csv(INPUT_FILE, sep=CSV_SEPARATOR, encoding="utf-8")
    print("File loaded successfully")
except FileNotFoundError:
    print("Error: file not found. Run add_indicators.py first")
    sys.exit(1)

# Виведення початкового DataFrame
print("\nInitial data:")
print(df)

# Базовий аналіз даних
print("\nFirst 3 rows of the DataFrame:")
print(df.head(3))

print("\nData types:")
print(df.dtypes)

print("\nDataFrame shape (rows, columns):")
print(df.shape)

print("\nDescriptive statistics:")
print(df.describe())

# Попереднє оброблення: зміна типів даних
df["Country Name"] = df["Country Name"].astype(str).str.strip()
df["Year"] = df["Year"].astype(int)
for column in (EXPORTS, GDP, POPULATION):
    # Нечислові значення стають NaN
    df[column] = pd.to_numeric(df[column], errors="coerce")

print("\nMissing values per column:")
print(df.isna().sum())

# Видаляємо рядки, де немає хоча б одного з показників
df = df.dropna(subset=[EXPORTS, GDP, POPULATION]).copy()
df[POPULATION] = df[POPULATION].astype("int64")
print("\nRows after removing missing values:", len(df))

# Додавання нового розрахункового стовпця:
# експорт товарів і послуг на одну особу (US$) = частка експорту у ВВП * ВВП на душу населення
df["Exports_per_capita_USD"] = (df[EXPORTS] / 100 * df[GDP]).round(2)

# Додавання категорії країни за рівнем ВВП на душу населення
df["GDP_group"] = pd.cut(df[GDP], bins=GDP_BINS, labels=GDP_LABELS)

print("\nDataFrame with new columns:")
print(df)

# Фільтрація даних: записи, де експорт більший за заданий поріг
filtered_df = df[df[EXPORTS] > EXPORTS_THRESHOLD]
print(f"\nFiltering result (exports > {EXPORTS_THRESHOLD}% of GDP):")
print(filtered_df)
print("Number of records:", len(filtered_df))

# Сортування даних за показником експорту (від більшого до меншого)
sorted_df = df.sort_values(by=EXPORTS, ascending=False)
print("\nTop 10 records by exports:")
print(sorted_df[["Country Name", "Year", EXPORTS]].head(10))

# Групування даних за роком: середнє, максимальне та мінімальне значення експорту
grouped_by_year = df.groupby("Year")[EXPORTS].agg(["mean", "max", "min"]).round(2)
print("\nExports by year (mean, max, min):")
print(grouped_by_year)

# Групування за групою ВВП на душу населення
grouped_by_group = df.groupby("GDP_group", observed=True).agg(
    countries=("Country Name", "nunique"),
    mean_exports=(EXPORTS, "mean"),
    mean_exports_per_capita=("Exports_per_capita_USD", "mean"),
).round(2)
print("\nStatistics by GDP group:")
print(grouped_by_group)

# Кількість унікальних значень у вибраних стовпцях
print("\nUnique countries:", df["Country Name"].nunique())
print("Unique years:", df["Year"].nunique())

# Збереження результатів аналізу у нові CSV-файли
sorted_df.to_csv(ANALYSIS_FILE, sep=CSV_SEPARATOR, index=False, encoding="utf-8")
grouped_by_group.to_csv(GROUPED_FILE, sep=CSV_SEPARATOR, encoding="utf-8")
print(f"\nResults saved to {ANALYSIS_FILE} and {GROUPED_FILE}")
