from nltk.probability import FreqDist
from nltk.stem import PorterStemmer

import text_loader

words = text_loader.load_words()
cleaned = text_loader.clean_words(words)

# Стемінг: приведення слів до їхньої основи
stemmer = PorterStemmer()
stems = [stemmer.stem(word) for word in cleaned]

# Приклади перетворення слів
print("Stemming examples:")
for word in cleaned[:10]:
    print(f"{word} -> {stemmer.stem(word)}")

# 10 найбільш уживаних основ слів
fdist = FreqDist(stems)
top_ten = fdist.most_common(10)

print("\n10 most common stems:")
for stem, count in top_ten:
    print(f"{stem}: {count}")
