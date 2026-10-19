# AI-Powered Dataset Analyzer

A Streamlit app for exploring CSV and Excel datasets. Upload a file to inspect its contents, review data quality and descriptive statistics, create a chart, and download the analyzed data as CSV.

## Requirements

- Python 3.8 or newer
- pip

## Setup

Open a terminal in the project directory and install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the app

```bash
streamlit run app.py
```

Streamlit will print a local URL in the terminal, typically <http://localhost:8501>. Open it in a browser to use the analyzer.

## Use

1. Upload a `.csv` or `.xlsx` file.
2. Review the dataset preview, row and column counts, missing-value count, data-quality table, and statistical summary.
3. Choose a chart type: histogram, bar chart, or scatter plot. Charts use numeric columns; scatter plots require at least two numeric columns.
4. Review the automatic summary insights and calculation checks.
5. Use **Download Dataset as CSV** to export the data.

The included `studentperformance.csv` file can be used as sample input.
