from nltk.probability import FreqDist

import text_loader

words = text_loader.load_words()

# Видалення стоп-слів і пунктуації
cleaned = text_loader.clean_words(words)
print("Words before cleaning:", len(words))
print("Words after removing stop words and punctuation:", len(cleaned))
print("First 20 words:", cleaned[:20])

# 10 найбільш уживаних слів після очищення
fdist = FreqDist(cleaned)
top_ten = fdist.most_common(10)

print("\n10 most common words after cleaning:")
for word, count in top_ten:
    print(f"{word}: {count}")

# Побудова стовпчастої діаграми
text_loader.plot_top_words(
    top_ten,
    "10 most common words after removing stop words and punctuation",
    "top10_cleaned.png",
)
