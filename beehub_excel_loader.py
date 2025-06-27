"""
beehub_excel_loader.py

This script loads telemetry data from Excel files exported via https://beehub.app.
It processes and cleans the dataset, extracts time features, and handles sensor error codes (-2137).

Author: Sebastian Górecki
Project: BeeHUB-IoT-Platform
"""

import os
import pandas as pd
import numpy as np
from tabulate import tabulate

# --- CONFIGURATION ---
data_folder = "./sample_data"  # Change this to your local path

file_names = sorted([
    os.path.join(data_folder, f)
    for f in os.listdir(data_folder)
    if f.endswith(".xlsx")
])[:5]

dataframes = []

for file_name in file_names:
    try:
        df = pd.read_excel(file_name)
        df.rename(columns={"Time (UTC+0)": "Date"}, inplace=True)
        df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y, %H:%M:%S", errors="coerce", dayfirst=True)

        columns_to_drop = [
            "rainfallOp", "windForce", "windMin", "windMax", "windAvg",
            "windMean", "windMode", "windForceMax", "windForceAve",
            "bhDewPoint", "bhTw", "bhwbgt", "bhDeltaT", "bhvpd",
            "b_Apparent_Temp", "Microprocessor temperature"
        ]
        df.drop(columns_to_drop, axis=1, errors="ignore", inplace=True)

        df["Device"] = os.path.basename(file_name).split(".")[0]

        df["weekday"] = df["Date"].dt.weekday
        df["month"] = df["Date"].dt.month
        df["day"] = df["Date"].dt.day
        df["year"] = df["Date"].dt.year
        df["hour"] = df["Date"].dt.hour
        df["minute"] = df["Date"].dt.minute

        dataframes.append(df)

    except Exception as e:
        print(f"[⚠️] Error processing {file_name}: {e}")

combined_df = pd.concat(dataframes, ignore_index=True)

if "Device" in combined_df.columns:
    print("✅ Hive data successfully labeled. Sample:")
    print(tabulate(combined_df.head(), headers="keys", tablefmt="grid"))
else:
    print("⚠️ Warning: 'Device' column missing!")

try:
    error_columns = combined_df.columns[(combined_df == -2137).any()]
    error_rows = combined_df[(combined_df == -2137).any(axis=1)]

    if not error_rows.empty:
        print(f"⚠️ Found sensor error code (-2137) in columns: {list(error_columns)}")
        print(f"🔹 Rows affected: {len(error_rows)}")
    else:
        print("✅ No sensor error codes detected.")
except Exception as e:
    print(f"⚠️ Error checking for -2137: {e}")

combined_df.replace(-2137, np.nan, inplace=True)
print("✅ All -2137 values replaced with NaN.")
