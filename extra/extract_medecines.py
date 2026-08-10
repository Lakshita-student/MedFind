import json
import pandas as pd

with open("drug-label-0001-of-0013.json", "r", encoding="utf-8") as f:
    data = json.load(f)

medicine_names = []

for item in data["results"]:
    if "openfda" in item and "brand_name" in item["openfda"]:
        medicine_names.append(item["openfda"]["brand_name"][0])

df = pd.DataFrame(medicine_names, columns=["medicine_name"])
df.to_csv("medicines.csv", index=False)

print("Dataset created successfully!")
print("Total medicines:", len(medicine_names))
