# campus-energy-dashboard-arbaazali
## Capstone Project – Programming for Problem Solving using Python

### Submitted By:
Arbaaz ali 
2501410039
K. R. Mangalam University

## 1. Project Objective
The objective of this project is to build an automated end-to-end energy analysis system that helps the campus facilities team understand electricity consumption trends across buildings.  
This dashboard enables decision-makers to identify high-consumption buildings, peak load hours, and opportunities for energy savings.

## 2. Features Implemented
This project includes the following key components:

### A. Data Ingestion and Validation
- Automatically reads multiple CSV files from the `/data/` folder using `pathlib`.
- Handles missing or corrupt files with exception handling.
- Adds metadata such as the building name.
- Merges all data into a cleaned combined DataFrame.

### B. Aggregation Logic
- Daily and weekly consumption calculated using `.resample()`
- Building-wise summary generated using `.groupby()`
- Stores summary in DataFrames and dictionaries

### C. Object-Oriented Programming
Implemented three classes:
1. `Building`
2. `MeterReading`
3. `BuildingManager`

These classes model buildings and their meter readings and generate building-level reports.

### D. Visualization Dashboard (Matplotlib)
Generated a multi-chart figure including:
1. Daily consumption trend line  
2. Weekly average comparison bar chart  
3. Peak-hour scatter plot  

All graphs are combined into one dashboard and saved as `dashboard.png`.

### E. Persistence and Summary
Exports:
- Cleaned dataset (`cleaned_energy_data.csv`)
- Building summary (`building_summary.csv`)
- Executive summary report (`summary.txt`)

## 3. Dataset Description
Each CSV file contains:
- `timestamp`: date and time of reading
- `kwh`: electricity consumed at that moment
- The filename identifies the building (e.g., `hostel.csv`, `library.csv`)

## 4. How to Run the Project

### Step 1: Install Dependencies

### Step 2: Run the Script

### Step 3: View Outputs
Check the `/output/` folder for:
- summary.txt
- cleaned_energy_data.csv
- building_summary.csv

Check the project directory for:
- dashboard.png

## 4. Results & Insights (Example)
- Highest consuming building: Hostel  
- Peak load recorded at: 01:00 AM on 2025-01-02  
- Daily trend shows higher night-time consumption  
- Weekly usage indicates hostel has consistently high demand  

## 5. Folder Structure

## 6. Academic Integrity
This is an individual project.  
All code and analysis were written by me without copying from others.




