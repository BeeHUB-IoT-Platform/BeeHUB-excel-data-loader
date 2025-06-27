# BeeHUB Data Loader for Google Colab
# Author: Sebastian Górecki

import os
import pandas as pd
import numpy as np
from tabulate import tabulate

# ✅ Define the folder containing hive data files (Google Drive mount path)
data_folder = "/content/drive/MyDrive/Colab/dane_z_uli"

# ✅ List only the first 5 Excel files for faster processing
file_names = sorted([
    os.path.join(data_folder, f)
    for f in os.listdir(data_folder)
    if f.endswith(".xlsx")
])[:5]

# ✅ Initialize an empty list to store dataframes
dataframes = []

# ✅ Process each file and extract relevant data
for file_name in file_names:
    try:
        df = pd.read_excel(file_name)
        df.rename(columns={"Time (UTC+0)": "Date"}, inplace=True)
        df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y, %H:%M:%S", errors="coerce", dayfirst=True)

        df.drop([
            "rainfallOp", "windForce", "windMin", "windMax", "windAvg",
            "windMean", "windMode", "windForceMax", "windForceAve",
            "bhDewPoint", "bhTw", "bhwbgt", "bhDeltaT", "bhvpd",
            "b_Apparent_Temp", "Microprocessor temperature"
        ], axis=1, errors="ignore", inplace=True)

        df["Device"] = os.path.basename(file_name).split(".")[0]

        df["weekday"] = df["Date"].dt.weekday
        df["month"] = df["Date"].dt.month
        df["day"] = df["Date"].dt.day
        df["year"] = df["Date"].dt.year
        df["hour"] = df["Date"].dt.hour
        df["minute"] = df["Date"].dt.minute

        dataframes.append(df)

    except Exception as e:
        print(f"⚠️ Error processing {file_name}: {e}")

# ✅ Combine all dataframes into a single dataset
combined_df = pd.concat(dataframes, ignore_index=True)

# ✅ Verify 'Device' column exists
if "Device" in combined_df.columns:
    print("✅ Hive data successfully labeled. Sample data:")
    print(tabulate(combined_df.head(), headers="keys", tablefmt="grid"))
else:
    print("⚠️ Error: 'Device' column is missing in the dataset.")

# ✅ Identify columns containing -2137 error codes
try:
    error_columns = combined_df.columns[(combined_df == -2137).any()]
    error_rows = combined_df[(combined_df == -2137).any(axis=1)]

    if not error_rows.empty:
        print(f"⚠️ The value -2137 (sensor error code) was found in these columns: {list(error_columns)}")
        print(f"🔹 Number of rows with errors: {len(error_rows)}")
    else:
        print("✅ No -2137 error codes found in the dataset.")
except Exception as e:
    print(f"⚠️ Error: {e}")

# ✅ Replace -2137 values with NaN
try:
    combined_df.replace(-2137, np.nan, inplace=True)
    print("✅ All values of -2137 have been replaced with NaN.")
except Exception as e:
    print(f"⚠️ Error: {e}")
