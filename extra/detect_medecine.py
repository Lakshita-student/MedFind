import cv2
import pytesseract
import pandas as pd

# Set tesseract path (change if different)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ----------------------------
# Load Medicine Dataset
# ----------------------------

df = pd.read_csv("medicines.csv")

# Assume first column has medicine names
medicines = df.iloc[:,0].astype(str).str.lower().tolist()

print("Loaded", len(medicines), "medicines")

# ----------------------------
# Load Prescription Image
# ----------------------------

image_path = "prescription.png"

image = cv2.imread(image_path)

if image is None:
    print("Error: Image not found. Check file name.")
    exit()

# ----------------------------
# Image Preprocessing
# ----------------------------

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Increase contrast
gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)

# Blur
blur = cv2.GaussianBlur(gray,(5,5),0)

# Threshold
thresh = cv2.adaptiveThreshold(
    blur,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11,
    2
)

# ----------------------------
# OCR Text Extraction
# ----------------------------

config = r'--oem 3 --psm 6'

text = pytesseract.image_to_string(thresh, config=config)

print("\nExtracted Text:\n")
print(text)

# ----------------------------
# Detect Medicines
# ----------------------------

detected = []

for word in text.lower().split():
    word = word.strip()

    if word in medicines:
        detected.append(word)

print("\nDetected Medicines:")

if len(detected) == 0:
    print("No medicine detected")
else:
    for med in set(detected):
        print(med)

# ----------------------------
# Show Processed Image
# ----------------------------

cv2.imshow("Processed Image", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
