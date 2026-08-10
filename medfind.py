import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("pharmacy_dataset_old.csv")

# --- Summary Statistics ---
print("\nSummary Information")
print(f"Number of records: {len(df)}")

numeric_cols = ['latitude', 'longitude', 'stock']
for col in numeric_cols:
    min_val = df[col].min()
    max_val = df[col].max()
    avg_val = df[col].mean()
    print(f"{col}: Min = {min_val:.3f}, Max = {max_val:.3f}, Avg = {avg_val:.3f}")

# --- Scatter Plot ---
plt.figure(figsize=(10, 6))
plt.scatter(df['longitude'], df['latitude'], 
            s=df['stock']*5,  # size proportional to stock
            c='blue', alpha=0.6, edgecolors='black')

# Add labels for each pharmacy
for i, row in df.iterrows():
    plt.text(row['longitude'], row['latitude'], row['pharmacy_name'], fontsize=8)

plt.title("Pharmacy Locations in Chandigarh")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()