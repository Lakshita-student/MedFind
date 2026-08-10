from flask import Flask, render_template, request
import pandas as pd
import easyocr
import re
import os
from rapidfuzz import process, fuzz
from geopy.distance import geodesic

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- LOAD DATA ----------------

data = pd.read_csv("pharmacy_dataset.csv")
subs_data = pd.read_csv("medicine_dataset.csv")

# Load interaction dataset
interaction_data = pd.read_csv("medicine_interactions.csv")

interaction_data["medicine1"] = interaction_data["medicine1"].str.lower()
interaction_data["medicine2"] = interaction_data["medicine2"].str.lower()

# clean column names
subs_data.columns = subs_data.columns.str.strip().str.lower()

# ---------------- EMERGENCY MEDICINES ----------------

EMERGENCY_MEDICINES = [
    "insulin",
    "adrenaline",
    "nitroglycerin",
    "salbutamol",
    "atropine",
    "epinephrine",
    "dopamine",
    "amiodarone",
    "naloxone",
    "diazepam"
]

# ---------------- CLEAN MEDICINE NAME ----------------

def clean_medicine_name(name):

    name = str(name).lower()

    # remove numbers like 500, 650
    name = re.sub(r"\d+.*", "", name)

    # remove dosage forms
    forms = ["tablet","tab","capsule","cap","syrup","injection","oral","suspension"]
    for f in forms:
        name = name.replace(f,"")

    return name.strip()

# clean pharmacy dataset names
data["clean_name"] = data["medicine_name"].apply(clean_medicine_name)

# clean substitute dataset names
subs_data["clean_name"] = subs_data["name"].apply(clean_medicine_name)

medicine_list = data["clean_name"].unique().tolist()

# ---------------- OCR ----------------

reader = easyocr.Reader(['en'])

def extract_text(image_path):

    result = reader.readtext(image_path, detail=0)
    text = " ".join(result)

    print("OCR TEXT:", text)

    return text


# ---------------- DETECT MEDICINE ----------------

def detect_medicines(text):

    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]',' ',text)

    words = text.split()

    phrases = []

    for i in range(len(words)):

        phrases.append(words[i])

        if i < len(words)-1:
            phrases.append(words[i]+" "+words[i+1])

        if i < len(words)-2:
            phrases.append(words[i]+" "+words[i+1]+" "+words[i+2])

    detected = []

    for phrase in phrases:

        match = process.extractOne(
            phrase,
            medicine_list,
            scorer=fuzz.token_sort_ratio
        )

        if match:

            name, score, _ = match

            if score > 90:
                detected.append(name)

    detected = list(set(detected))

    print("Detected Medicines:", detected)

    return detected


# ---------------- SUBSTITUTE SEARCH ----------------

def get_substitutes(medicine):

    medicine = clean_medicine_name(medicine)

    matches = subs_data[
        subs_data["clean_name"].str.contains(medicine, na=False)
    ]

    substitutes = []

    for _,row in matches.iterrows():

        for i in range(5):

            col = f"substitute{i}"

            if col in row and pd.notna(row[col]):

                clean_sub = clean_medicine_name(row[col])

                substitutes.append(clean_sub)

    return list(set(substitutes))


#--------------------- EMERGENCY MEDICINE DETECTION ----------------

def detect_emergency_medicines(medicines):

    emergency_found = []

    for med in medicines:
        for e in EMERGENCY_MEDICINES:
            if e in med.lower():
                emergency_found.append(med)

    return list(set(emergency_found))


# ---------------- FIND PHARMACIES ----------------

def find_pharmacies(medicines,user_lat,user_lng):

    pharmacies = []

    for med in medicines:

        med = clean_medicine_name(med)

        matches = data[data["clean_name"] == med]

        for _,row in matches.iterrows():

            distance = geodesic(
                (user_lat,user_lng),
                (row["latitude"],row["longitude"])
            ).km

            pharmacies.append({

                "name":str(row["pharmacy_name"]),
                "address":str(row["address"]),
                "medicine":str(row["medicine_name"]),
                "stock":int(row["stock"]),
                "latitude":float(row["latitude"]),
                "longitude":float(row["longitude"]),
                "distance":float(round(distance,2)),
                "color": get_stock_color(row["stock"])

            })

    pharmacies = sorted(pharmacies,key=lambda x:x["distance"])

    return pharmacies[:10]



# ---------------- CHECK MEDICINE INTERACTIONS ----------------

def check_interactions(medicine_list):

    warnings = []
    seen_pairs = set()

    for i in range(len(medicine_list)):
        for j in range(i + 1, len(medicine_list)):

            m1 = medicine_list[i].lower()
            m2 = medicine_list[j].lower()

            pair = tuple(sorted([m1, m2]))

            if pair in seen_pairs:
                continue

            match = interaction_data[
                ((interaction_data["medicine1"] == m1) & (interaction_data["medicine2"] == m2)) |
                ((interaction_data["medicine1"] == m2) & (interaction_data["medicine2"] == m1))
            ]

            if not match.empty:

                row = match.iloc[0]  # take first match only

                warnings.append({
                    "med1": m1,
                    "med2": m2,
                    "severity": row["severity"],
                    "description": row["warning"]
                })

                seen_pairs.add(pair)

    return warnings

# ---------------- GET STOCK COLOR ----------------

def get_stock_color(stock):

    if stock <= 10:
        return "red"       # very low stock

    elif stock <= 30:
        return "yellow"    # medium stock

    else:
        return "green"     # high stock

# ---------------- ROUTE ----------------

@app.route("/",methods=["GET","POST"])

def index():

    interaction_warnings = []
    detected_medicines = []
    pharmacies = []
    substitutes = {}
    searched_substitutes = []
    show_pharmacies = False

    if request.method == "POST":

        medicine_input = request.form.get("medicine")
        lat = request.form.get("lat")
        lng = request.form.get("lng")
        action = request.form.get("action")

        if lat and lng:
            user_lat = float(lat)
            user_lng = float(lng)
        else:
            user_lat = 30.7333
            user_lng = 76.7794

        # TEXT SEARCH
        if medicine_input:
            detected_medicines = [
            clean_medicine_name(m.strip())
            for m in medicine_input.split(",")
            if m.strip() != ""
        ]

        # IMAGE SEARCH
        file = request.files.get("image")

        if file and file.filename != "":

            filepath = os.path.join(UPLOAD_FOLDER,file.filename)
            file.save(filepath)

            text = extract_text(filepath)
            detected_medicines = detect_medicines(text)

        # PROCESS MEDICINE
        if detected_medicines:

            interaction_warnings = check_interactions(detected_medicines)
            med = detected_medicines[0]

            matches = data[data["clean_name"] == med]

            # MEDICINE FOUND
            if not matches.empty:

                pharmacies = find_pharmacies(
                    [med],
                    user_lat,
                    user_lng
                )

                show_pharmacies = True

            # MEDICINE NOT FOUND
            else:

                subs = get_substitutes(med)

                valid_subs = [
                    s for s in subs
                    if s in medicine_list
                ]

                if action != "find_pharmacy":

                    if valid_subs:
                        substitutes[med] = valid_subs

                else:

                    if valid_subs:
                        searched_substitutes = valid_subs
                    else:
                        searched_substitutes = [med]

                    pharmacies = find_pharmacies(
                        searched_substitutes,
                        user_lat,
                        user_lng
                    )

                    show_pharmacies = True

    return render_template(
        "index.html",
        medicines=detected_medicines,
        pharmacies=pharmacies,
        substitutes=substitutes,
        searched_substitutes=searched_substitutes,
        show_pharmacies=show_pharmacies,
        interaction_warnings=interaction_warnings
    )


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
