import sys

import pandas as pd
import requests

# Файл із практичної роботи 5 та файл з додатковими показниками
BASE_FILE = "exports_gdp.csv"
OUTPUT_FILE = "exports_extended.csv"
CSV_SEPARATOR = ";"

# Період, який використовувався в практичній роботі 5
START_YEAR = 2018
END_YEAR = 2019

# Додаткові показники Світового банку: назва стовпця -> код показника
NEW_INDICATORS = {
    "GDP per capita (current US$)": "NY.GDP.PCAP.CD",
    "Population, total": "SP.POP.TOTL",
}

API_URL = "https://api.worldbank.org/v2/country/all/indicator/{code}"


# Функція завантажує показник Світового банку для всіх країн за вказаний період і повертає DataFrame зі стовпцями: Country Name, Year, <назва показника>
def fetch_indicator(code, column_name):
    params = {
        "date": f"{START_YEAR}:{END_YEAR}",
        "format": "json",
        "per_page": 1000,
    }
    response = requests.get(API_URL.format(code=code), params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Друга частина відповіді API містить список записів
    if len(data) < 2 or data[1] is None:
        raise ValueError(f"No data returned for indicator {code}")

    rows = []
    for item in data[1]:
        rows.append({
            "Country Name": item["country"]["value"],
            "Year": int(item["date"]),
            column_name: item["value"],
        })
    return pd.DataFrame(rows)


def main():
    # Завантаження основного файлу з практичної роботи 5
    try:
        df = pd.read_csv(BASE_FILE, sep=CSV_SEPARATOR, encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: file {BASE_FILE} not found. Run practical work 5 first.")
        sys.exit(1)

    df["Country Name"] = df["Country Name"].str.strip()
    print(f"Base file loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    # Додаємо кожен новий показник як окремий стовпець
    for column_name, code in NEW_INDICATORS.items():
        try:
            new_data = fetch_indicator(code, column_name)
        except (requests.RequestException, ValueError, KeyError) as error:
            print(f"Error while downloading {column_name}: {error}")
            sys.exit(1)

        # Об'єднуємо за країною та роком
        df = df.merge(new_data, on=["Country Name", "Year"], how="left")
        print(f"Column added: {column_name}")

    df.to_csv(OUTPUT_FILE, sep=CSV_SEPARATOR, index=False, encoding="utf-8")
    print(f"Extended data saved to {OUTPUT_FILE}: {df.shape[0]} rows, {df.shape[1]} columns")


if __name__ == "__main__":
    main()
