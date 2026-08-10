from fuzzywuzzy import process

# OCR detected text (example from your output)
ocr_words = ["Ajoct", "CSmulsen", "xibtn"]

# Medicine database
medicines = [
    "Azopt",
    "Combigan",
    "Xalatan",
    "Paracetamol",
    "Amoxicillin",
    "Dolo 650",
    "Crocin",
    "Augmentin"
]

print("Corrected Medicines:\n")

for word in ocr_words:
    match = process.extractOne(word, medicines)
    print(f"OCR word: {word}")
    print(f"Predicted Medicine: {match[0]} (confidence {match[1]}%)\n")
