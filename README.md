# 💊 MedFind – AI-Powered Medicine Finder

MedFind is an AI-powered medicine search and pharmacy locator application designed to help users find medicines and locate nearby pharmacies. It combines OCR, intelligent text matching, and location-based services to make medicine discovery easier and more accessible.

## 🚀 Features

* **Medicine Search:** Search for medicines using the available medicine dataset.
* **Prescription Image Recognition:** Extract medicine names from prescription images using OCR.
* **Intelligent Matching:** Identify medicine names using fuzzy string matching.
* **Nearby Pharmacy Locator:** Find pharmacies based on the user's location.
* **Medicine Availability:** View medicine stock information from the pharmacy dataset.
* **Interactive Map:** Visualize nearby pharmacies using Leaflet and OpenStreetMap.

## 🛠️ Tech Stack

| Category                | Technologies                  |
| ----------------------- | ----------------------------- |
| Backend                 | Python, Flask                 |
| Frontend                | HTML, CSS, JavaScript         |
| OCR                     | EasyOCR                       |
| Text Matching           | RapidFuzz                     |
| Data Processing         | Pandas                        |
| Maps & Location         | Leaflet, OpenStreetMap, Geopy |
| Database / Data Storage | CSV datasets                  |

## 📂 Project Structure

```text
MedFind/
│
├── app.py
├── medfind.py
├── find_pharmacy.py
├── ocr_reader.py
│
├── medicine_dataset.csv
├── medicine_interactions.csv
├── pharmacy_dataset.csv
│
├── templates/
├── static/
├── extra/
│
├── .gitignore
├── .gitattributes
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Lakshita-student/MedFind.git
cd MedFind
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Open the local URL displayed in your terminal, usually:

```text
http://127.0.0.1:5000/
```

## 📊 Datasets

The project uses the following datasets:

* `medicine_dataset.csv` – Medicine information.
* `medicine_interactions.csv` – Medicine interaction information.
* `pharmacy_dataset.csv` – Pharmacy details and medicine stock information.

**Note:** The large medicine dataset is managed using Git Large File Storage (Git LFS). Install Git LFS before cloning if you want to retrieve the full dataset.

## 🔮 Future Improvements

* Medicine alternative recommendations.
* Medicine shortage prediction.
* Improved prescription recognition.
* Expanded pharmacy and medicine coverage.

## ⚠️ Disclaimer

MedFind is an educational and informational project. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional before making medication-related decisions.

## 👩‍💻 Developed By

**Lakshita Khaneja**

GitHub: [Lakshita-student](https://github.com/Lakshita-student)

---

⭐ If you find this project interesting, consider giving the repository a star!
