import string

import matplotlib.pyplot as plt
import nltk
from nltk.corpus import gutenberg, stopwords

TEXT_FILE = "shakespeare-caesar.txt"


# Функція завантажує потрібні ресурси NLTK (якщо їх ще немає)
def download_resources():
    for resource in ("gutenberg", "stopwords"):
        nltk.download(resource, quiet=True)


# Функція повертає список усіх слів тексту з Project Gutenberg
def load_words():
    download_resources()
    return list(gutenberg.words(TEXT_FILE))


# Функція видаляє зі списку стоп-слова та пунктуацію, слова переводить у нижній регістр
def clean_words(words):
    stop_words = set(stopwords.words("english"))
    table = str.maketrans("", "", string.punctuation)

    cleaned = []
    for word in words:
        word = word.lower()
        if word in stop_words:
            continue
        # Видаляємо розділові знаки всередині слова
        word = word.translate(table)
        # Залишаємо тільки слова з літер, які не є стоп-словами
        if word.isalpha() and word not in stop_words:
            cleaned.append(word)
    return cleaned


# Функція будує стовпчасту діаграму за списком пар (слово, кількість)
def plot_top_words(top_words, title, filename):
    labels = [pair[0] for pair in top_words]
    counts = [pair[1] for pair in top_words]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, counts, color="steelblue")

    # Підписуємо значення над стовпцями
    for i, count in enumerate(counts):
        plt.text(i, count, str(count), ha="center", va="bottom", fontsize=10)

    plt.title(title, fontsize=14)
    plt.xlabel("Word", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()
