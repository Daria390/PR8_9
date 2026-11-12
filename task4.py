from nltk.probability import FreqDist

import text_loader

words = text_loader.load_words()

# Частота слів і 10 найбільш уживаних
fdist = FreqDist(words)
top_ten = fdist.most_common(10)

print("10 most common words:")
for word, count in top_ten:
    print(f"{word!r}: {count}")

# Побудова стовпчастої діаграми
text_loader.plot_top_words(
    top_ten,
    "10 most common words in 'Julius Caesar'",
    "top10_raw.png",
)
