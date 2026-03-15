# Scalable Data Processing and Analytics Pipeline

## Overview
This repository contains a production-quality, modular Python pipeline for data ingestion, cleaning, transformation, analytics, graph analysis, and visualization. It is designed to take raw CSV data and output clean, transformed datasets along with comprehensive analytics reports and visual graphs.

## System Architecture

The project consists of multiple independent modules:
- **`pipeline.ingestion`**: Loads datasets from CSVs, logs shapes and data types.
- **`pipeline.cleaning`**: Removes duplicate rows, handles missing data (median for numeric, mode for categorical), and caps outliers using the IQR method.
- **`pipeline.transformation`**: Standardizes/Normalizes numerical features, encodes categorical variables, and generates new features.
- **`pipeline.analytics`**: Computes descriptive statistics, column distributions, variance-based feature importance, and correlation matrices.
- **`pipeline.graph_analysis`**: Builds a NetworkX graph representation of feature relationships based on correlation thresholds and provides BFS/DFS traversals.
- **`pipeline.visualization`**: Generates histograms, scatter plots, feature distributions, and a correlation heatmap using Matplotlib and Seaborn.
- **`pipeline.report`**: Aggregates all findings into a final text report (`report.txt`).

## Folder Structure
```
data_pipeline_project/
├── main.py                  # Main runner to execute the pipeline sequentially
├── README.md                # Project documentation
├── data/
│   ├── raw/                 # Put your raw CSV files here
│   └── processed/           # Processed datasets, reports, and visualizations
├── pipeline/
│   ├── ingestion/           # CSV Loading Logic
│   ├── cleaning/            # Cleaning Engine
│   ├── transformation/      # Feature Engineering & Transformation
│   ├── analytics/           # Analytics Engine
│   ├── graph_analysis/      # NetworkX Graph Logic
│   ├── visualization/       # Matplotlib Visual Engine
│   ├── report/              # Final Report Generator
│   └── utils/               # File and Logging Utilities
└── tests/                   # Unit test suite
```

## Installation Instructions

1. Ensure you have Python 3.8+ installed.
2. Clone this repository (or copy the `data_pipeline_project` folder).
3. Install the required dependencies:
   ```bash
   pip install pandas numpy matplotlib seaborn networkx scikit-learn
   ```

## Example Usage

Run the pipeline using the `main.py` entry point. Pass the path to your CSV file as an argument:

```bash
python main.py data/raw/your_dataset.csv
```

The system will:
1. Load and log the dataset properties.
2. Clean and handle outliers/missing values.
3. Transform features (standardize & encode).
4. Perform analytical processing.
5. Create a correlation graph representation.
6. Generate visualizations (saved to `data/processed/visualizations/`).
7. Save a final summary report to `data/processed/report/report.txt`.
8. Save the cleaned and transformed data to `data/processed/processed_dataset.csv`.

To run the unit tests:
```bash
python -m unittest discover tests/
```
