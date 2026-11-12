import text_loader

# Завантаження тексту "Julius Caesar" В. Шекспіра
words = text_loader.load_words()

# Загальна кількість слів (токенів), разом із розділовими знаками
total_words = len(words)

# Кількість унікальних слів
unique_words = len(set(words))

# Унікальні слова без урахування регістру
unique_lower = len(set(word.lower() for word in words))

print("Text:", text_loader.TEXT_FILE)
print("Total number of words:", total_words)
print("Number of unique words:", unique_words)
print("Number of unique words (case-insensitive):", unique_lower)

# Порівняння значень
print("\nDifference:", total_words - unique_words)
print(f"Unique words make up {unique_words / total_words * 100:.2f}% of the text")
print(f"On average, each unique word is used {total_words / unique_words:.2f} times")
