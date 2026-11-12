import calendar
import sys

import matplotlib.pyplot as plt
import pandas as pd

CSV_FILE = "2013.csv"
YEAR = 2013

# Ключові слова для пошуку трьох обраних велодоріжок у назвах стовпців
SELECTED_KEYWORDS = ["berri", "maisonneuve", "parc"]
PLOT_FILE = "bike_path_2013.png"

plt.style.use("ggplot")


# Функція залишає в назві тільки літери й цифри в нижньому регістрі, щоб "Maisonneuve_1" і "Maisonneuve 1" вважалися однаковими
def normalize(name):
    return "".join(symbol for symbol in str(name).lower() if symbol.isalnum())


# Функція знаходить у DataFrame три велодоріжки за ключовими словами
# Якщо якусь не знайдено, замість неї беремо найбільш завантажену з решти
def find_paths(df, keywords):
    selected = []
    for keyword in keywords:
        for column in df.columns:
            if keyword in normalize(column) and column not in selected:
                selected.append(column)
                break

    if len(selected) < len(keywords):
        busiest = df.sum().sort_values(ascending=False).index
        for column in busiest:
            if len(selected) == len(keywords):
                break
            if column not in selected:
                selected.append(column)
        print("Note: some bike paths were not found by name, busiest paths were added")
    return selected


# Завантаження даних: роздільник визначається автоматично, дата стає індексом
try:
    df = pd.read_csv(
        CSV_FILE,
        sep=None,
        engine="python",
        encoding="utf-8-sig",
        parse_dates=["Date"],
        dayfirst=True,
        index_col="Date",
    )
except FileNotFoundError:
    print(f"Error: file {CSV_FILE} not found")
    sys.exit(1)
except (KeyError, ValueError) as error:
    print("Error: wrong file structure (column 'Date' is expected):", error)
    sys.exit(1)

# Прибираємо службові й порожні стовпці, значення перетворюємо на числа
df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]
df = df.apply(pd.to_numeric, errors="coerce").dropna(axis=1, how="all")

# Приводимо індекс до формату дат (формат визначається автоматично)
raw = df.index.astype(str).str.strip()
df.index = pd.to_datetime(raw, dayfirst=not raw[0][:4].isdigit(), errors="coerce")
df = df[df.index.notna()]

# Залишаємо тільки дані за вибраний рік
df = df[df.index.year == YEAR]

# Первинний аналіз DataFrame
print("First rows:")
print(df.head())
print("\nDataFrame info:")
df.info()
print("\nDescriptive statistics:")
print(df.describe())

# Загальна кількість велосипедистів за рік для кожної велодоріжки та для всіх разом
totals = df.sum().sort_values(ascending=False)
print(f"\nTotal cyclists in {YEAR} for each bike path:")
print(totals.astype(int))
print(f"\nTotal cyclists in {YEAR} for all bike paths: {int(totals.sum())}")

# Найбільш популярний місяць для трьох обраних велодоріжок
paths = find_paths(df, SELECTED_KEYWORDS)
print("\nSelected bike paths:", paths)

# Групування за номером місяця й підсумовування кількості велосипедистів
monthly = df[paths].groupby(df.index.month).sum()
monthly.index = [calendar.month_name[month] for month in monthly.index]
print("\nCyclists by month:")
print(monthly)

print("\nMost popular month for each selected path:")
for path in paths:
    best_month = monthly[path].idxmax()
    print(f"{path}: {best_month} ({int(monthly[path].max())} cyclists)")

# Динаміка використання однієї з велодоріжок (перша з обраних)
main_path = paths[0]
dynamics = monthly[main_path]
change = (dynamics.pct_change() * 100).round(1)
print(f"\nMonthly dynamics for {main_path} (change to previous month, %):")
print(pd.DataFrame({"cyclists": dynamics.astype(int), "change_%": change}))

# Побудова графіка зміни кількості велосипедистів за місяцями
plt.figure(figsize=(10, 5))
plt.plot(range(1, len(dynamics) + 1), dynamics.values, marker="o", color="steelblue")
plt.xticks(range(1, len(dynamics) + 1), [name[:3] for name in dynamics.index])
plt.title(f"Number of cyclists on {main_path} by month, {YEAR}", fontsize=14)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Number of cyclists", fontsize=12)
plt.tight_layout()
plt.savefig(PLOT_FILE)
plt.show()