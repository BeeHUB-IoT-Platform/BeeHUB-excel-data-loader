# BeeHUB IoT Platform – Excel Data Loader

This repository provides a Python script to load and preprocess telemetry data from beehives using the [BeeHUB Platform](https://beehub.app). Data is exported from Excel files downloaded via the [Intelligent Hives](https://intelligenthives.eu) system.

## Features

- 🐝 Loads multiple Excel files containing hive telemetry
- 🕒 Extracts timestamp-based features (weekday, hour, etc.)
- 🧹 Cleans unused sensor data columns
- ❗ Replaces sensor error codes (e.g. `-2137`) with `NaN`
- 🗂 Tags data with hive/device identifiers

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/BeeHUB-IoT-Platform.git
   cd BeeHUB-IoT-Platform
   ```

2. Install dependencies:
   ```bash
   pip install pandas numpy tabulate openpyxl
   ```

3. Place your `.xlsx` files in the `./sample_data/` directory.

4. Run the loader:
   ```bash
   python beehub_excel_loader.py
   ```

## Sample Output

```
✅ Hive data successfully labeled. Sample:
+----+---------------------+---------+--------+ ... +--------+
|    | Date                | weight  | temp1  | ... | Device |
+----+---------------------+---------+--------+-----+--------+
| 0  | 2024-06-01 05:00:00 | 43250.0 | 25.8   | ... | BH123  |
...
```

## About

This project is part of the ongoing work in **BeeHUB**, a smart telemetry and analytics platform for monitoring beehives. Developed by **Sebastian Górecki** @ [IntelligentHives.eu](https://intelligenthives.eu)
