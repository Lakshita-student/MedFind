import pandas as pd
from geopy.distance import geodesic

# Load dataset
data = pd.read_csv("pharmacy_dataset.csv")

# User location (example location)
user_location = (30.7333, 76.7794)

# Ask user for medicine
medicine = input("Enter medicine name: ").strip().lower()

# Filter pharmacies that have the medicine
filtered = data[data["medicine_name"].str.lower() == medicine]

if filtered.empty:
    print("Medicine not found in dataset")
else:
    
    pharmacies = []

    for index, row in filtered.iterrows():

        pharmacy_location = (row["latitude"], row["longitude"])

        distance = geodesic(user_location, pharmacy_location).km

        pharmacies.append({
            "pharmacy": row["pharmacy_name"],
            "address": row["address"],
            "distance": round(distance,2),
            "stock": row["stock"]
        })

    pharmacies = sorted(pharmacies, key=lambda x: x["distance"])

    print("\nNearby Pharmacies:\n")

    for p in pharmacies:
        print(
            f"{p['pharmacy']} | {p['address']} | {p['distance']} km | Stock: {p['stock']}"
        )
