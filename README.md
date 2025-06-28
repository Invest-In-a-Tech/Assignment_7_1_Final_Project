# Final Project: Statistical Data Science

## Students
- **Olivia Anderson**
- **Roy Williams**

---

## Project Overview
This project demonstrates the complete data science workflow, from data acquisition and exploratory data analysis (EDA) to statistical analysis, machine learning modeling, and interactive visualizations. The goal is to analyze worldwide vaccination data, extract insights, and build a predictive model to classify countries as "well-vaccinated" or "poorly-vaccinated" based on their features.

---

## Table of Contents
- [Project Structure](#project-structure)
- [1. Exploratory Data Analysis (EDA)](#1-exploratory-data-analysis-eda)
- [2. Statistical Analysis](#2-statistical-analysis)
- [3. Machine Learning Modeling](#3-machine-learning-modeling)
- [4. Visualizations](#4-visualizations)
- [5. Interactive Dashboard (Streamlit)](#5-interactive-dashboard-streamlit)
- [6. Getting Started](#6-getting-started)
- [7. Project Organization](#7-project-organization)
- [8. Requirements](#8-requirements)
- [9. How to Run](#9-how-to-run)

---

## Project Structure
```
├── app.py                  # Streamlit dashboard for interactive EDA
├── requirements.txt        # Python dependencies
├── data/                   # Data folders (raw, processed, etc.)
├── notebooks/              # Jupyter notebooks for EDA and prototyping
├── src/                    # Source code (data processing, features, modeling)
└── ...
```

---

## 1. Exploratory Data Analysis (EDA)
- Loaded and cleaned the worldwide vaccination dataset.
- Explored data structure, types, and missing values.
- Visualized distributions and relationships between variables.
- Used interactive tables and charts for deeper insights.

## 2. Statistical Analysis
- Computed summary statistics (mean, median, mode, etc.).
- Analyzed correlations between features.
- Identified patterns and outliers in the data.

## 3. Machine Learning Modeling
- Defined a classification problem: predict if a country is "well-vaccinated" or "poorly-vaccinated" based on a threshold of % fully vaccinated.
- Engineered features and created target labels.
- Split data into training and test sets.
- Trained a logistic regression model.
- Evaluated model performance using classification report, confusion matrix, and accuracy score.

## 4. Visualizations
- Used Plotly and Altair for interactive and publication-quality charts:
  - Histograms, bar charts, and heatmaps for EDA.
  - Model performance visualizations (metrics, confusion matrix, accuracy gauge).
- All visualizations are available in the Jupyter notebook and Streamlit dashboard.

## 5. Interactive Dashboard (Streamlit)
- `app.py` provides a user-friendly dashboard for:
  - Uploading your own CSV/Excel data
  - Exploring data with interactive tables and plots
  - Analyzing columns, distributions, and correlations
  - Downloading processed data
- Powered by Plotly and Altair for beautiful, responsive visualizations.

---

## 6. Getting Started
### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Statistical-Data-Science/Assignment_7_1_Final_Project
```

### 2. Create a Virtual Environment (Recommended)
On Windows (PowerShell):
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```
On macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

---

## 7. Project Organization
- **notebooks/**: Jupyter notebooks for EDA, prototyping, and reporting.
- **src/**: Modular Python code for data processing, feature engineering, and modeling.
- **data/**: Organized data folders (raw, processed, features, etc.).
- **app.py**: Streamlit dashboard for interactive EDA and visualization.

---

## 8. Requirements
- Python 3.8+
- See `requirements.txt` for all dependencies (pandas, numpy, plotly, altair, scikit-learn, streamlit, etc.)

---

## 9. How to Run
### Run the Streamlit Dashboard
```bash
streamlit run app.py
```
- Open the provided local URL in your browser to access the dashboard.
- Upload your own data or explore the provided dataset.

### Run Jupyter Notebooks
```bash
jupyter notebook
```
- Open and run the notebooks in the `notebooks/` folder for step-by-step analysis and code.

---

**Enjoy exploring and analyzing data!**
