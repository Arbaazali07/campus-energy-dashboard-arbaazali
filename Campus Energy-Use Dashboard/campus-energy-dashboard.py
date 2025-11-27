# Capstone Project: Campus Energy-Use Dashboard
# Course: Programming for Problem Solving using Python
# Author: <Arbaaz ali>
# Date: <4th december 2025>
#
# Description:
# This script reads multiple building energy meter CSV files, validates them,
# aggregates consumption using functions and Pandas groupby/resample,
# models buildings using object-oriented design,
# produces a multi-chart energy dashboard,
# exports cleaned and summarized data,
# and generates an executive summary.
#
# Folder structure:
# /data/              -> input CSV files (one per building)
# /output/            -> results, plots, summary
#
# Requirements:
# pip install pandas numpy matplotlib


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os


# ------------------------------------------------------
# Task 1: Data Ingestion and Validation
# ------------------------------------------------------

def load_all_building_data(data_folder="data"):
    """
    Reads all CSV files inside /data/ and merges them into a single DataFrame.
    Adds building names, validates missing data, and logs problems.
    """

    data_path = Path(data_folder)
    if not data_path.exists():
        print("Data folder not found.")
        return pd.DataFrame()

    all_files = list(data_path.glob("*.csv"))
    if not all_files:
        print("No CSV files found inside /data/.")
        return pd.DataFrame()

    combined_df = []
    print("Starting data ingestion...")

    for file in all_files:
        try:
            df = pd.read_csv(file, on_bad_lines="skip")
            df['Building'] = file.stem

            # Validate timestamp column
            if 'timestamp' not in df.columns:
                print(f"Missing timestamp column in {file.name}. Skipping file.")
                continue

            # Validate kWh column
            if 'kwh' not in df.columns:
                print(f"Missing kwh column in {file.name}. Skipping file.")
                continue

            # Convert timestamp
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df = df.dropna(subset=['timestamp'])

            combined_df.append(df)

        except FileNotFoundError:
            print(f"File not found: {file}")
        except Exception as e:
            print(f"Error reading {file}: {e}")

    if not combined_df:
        print("No valid files were loaded.")
        return pd.DataFrame()

    df_combined = pd.concat(combined_df, ignore_index=True)
    df_combined = df_combined.sort_values(by="timestamp")

    print("Data ingestion completed.")
    return df_combined


# ------------------------------------------------------
# Task 2: Aggregation Logic
# ------------------------------------------------------

def calculate_daily_totals(df):
    """
    Returns daily energy totals for the entire campus.
    """
    df = df.set_index("timestamp")
    daily = df['kwh'].resample('D').sum()
    return daily


def calculate_weekly_aggregates(df):
    """
    Returns weekly electricity usage totals.
    """
    df = df.set_index("timestamp")
    weekly = df['kwh'].resample('W').sum()
    return weekly


def building_wise_summary(df):
    """
    Returns summary statistics (mean, min, max, total)
    for each building.
    """
    summary = df.groupby("Building")['kwh'].agg(
        Mean='mean',
        Min='min',
        Max='max',
        Total='sum'
    )

    return summary


# ------------------------------------------------------
# Task 3: Object-Oriented Modeling
# ------------------------------------------------------

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh


class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, reading: MeterReading):
        self.meter_readings.append(reading)

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.meter_readings)

    def generate_report(self):
        total = self.calculate_total_consumption()
        return f"Building: {self.name} | Total Consumption: {total} kWh"


class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def add_reading(self, building_name, timestamp, kwh):
        if building_name not in self.buildings:
            self.buildings[building_name] = Building(building_name)
        reading = MeterReading(timestamp, kwh)
        self.buildings[building_name].add_reading(reading)

    def generate_all_reports(self):
        reports = []
        for building in self.buildings.values():
            reports.append(building.generate_report())
        return reports


# ------------------------------------------------------
# Task 4: Visualization (Dashboard)
# ------------------------------------------------------

def create_dashboard(df, daily, weekly, summary):
    """
    Produces a multi-chart dashboard:
    1. Trend line of daily totals
    2. Bar chart of weekly averages per building
    3. Scatter plot of peak-hours usage (example: top 200 values)
    """

    plt.figure(figsize=(15, 12))

    # Plot 1: Daily consumption trend
    ax1 = plt.subplot(3, 1, 1)
    ax1.plot(daily.index, daily.values, color='blue')
    ax1.set_title("Daily Energy Consumption (All Buildings)")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("kWh")

    # Plot 2: Weekly averages per building (bar chart)
    building_weekly = df.copy()
    building_weekly = building_weekly.set_index("timestamp")
    building_weekly = building_weekly.groupby("Building")['kwh'].resample('W').sum().groupby("Building").mean()

    ax2 = plt.subplot(3, 1, 2)
    ax2.bar(building_weekly.index, building_weekly.values, color='green')
    ax2.set_title("Average Weekly Usage per Building")
    ax2.set_xlabel("Building")
    ax2.set_ylabel("Average Weekly kWh")

    # Plot 3: Scatter plot of peak-hour values
    top_values = df.sort_values(by="kwh", ascending=False).head(200)
    ax3 = plt.subplot(3, 1, 3)
    ax3.scatter(top_values['timestamp'], top_values['kwh'], alpha=0.6)
    ax3.set_title("Peak-hour Consumption Scatter Plot")
    ax3.set_xlabel("Timestamp")
    ax3.set_ylabel("kWh")

    plt.tight_layout()
    plt.savefig("dashboard.png")
    plt.close()
    print("Dashboard saved as dashboard.png")


# ------------------------------------------------------
# Task 5: Persistence and Executive Summary
# ------------------------------------------------------

def export_results(df, summary, daily, weekly):
    """
    Saves cleaned dataset, summary table, and analysis report.
    """

    output_folder = Path("output")
    output_folder.mkdir(exist_ok=True)

    df.to_csv(output_folder / "cleaned_energy_data.csv", index=False)
    summary.to_csv(output_folder / "building_summary.csv")

    total_consumption = df['kwh'].sum()
    highest_building = summary['Total'].idxmax()
    peak_load_row = df.loc[df['kwh'].idxmax()]
    peak_time = peak_load_row['timestamp']

    with open(output_folder / "summary.txt", "w") as f:
        f.write("Campus Energy Dashboard Summary\n")
        f.write("---------------------------------\n")
        f.write(f"Total Campus Consumption: {total_consumption} kWh\n")
        f.write(f"Highest Consuming Building: {highest_building}\n")
        f.write(f"Peak Load Time: {peak_time}\n")
        f.write(f"Daily Trend Sample: {daily.head()}\n")
        f.write(f"Weekly Trend Sample: {weekly.head()}\n")

    print("Summary and CSV files exported to /output/ folder.")


# ------------------------------------------------------
# Main Program
# ------------------------------------------------------

def main():
    df = load_all_building_data("data")
    if df.empty:
        print("No data available. Ending program.")
        return

    daily = calculate_daily_totals(df)
    weekly = calculate_weekly_aggregates(df)
    summary = building_wise_summary(df)

    manager = BuildingManager()
    for _, row in df.iterrows():
        manager.add_reading(row['Building'], row['timestamp'], row['kwh'])

    reports = manager.generate_all_reports()
    print("Building Reports:")
    for r in reports:
        print(r)

    create_dashboard(df, daily, weekly, summary)
    export_results(df, summary, daily, weekly)

    print("Project completed successfully.")


if __name__ == "__main__":
    main()
