# Heart Attack Risk Analysis

## 📌 Project Overview
The **Heart Attack Risk Analysis** project is a comprehensive web-based platform designed to analyze and visualize heart health data. Leveraging the power of **Python**, **Flask**, **Pandas**, and **NumPy**, this application provides deep insights into various risk factors contributing to heart attacks, such as age, cholesterol levels, blood pressure, and lifestyle choices.

The application features an interactive dashboard with data visualizations, detailed statistical insights, and a dedicated analysis section powered by advanced NumPy calculations.

## 🚀 Features

### 1. Interactive Dashboard
- **Data Overview:** Real-time summary of the dataset, including total records, features, and attribute details.
- **Sample Data:** Preview of the raw dataset for transparency.

### 2. Advanced Visualizations
Explore a variety of interactive plots generated using **Matplotlib** and **Seaborn**:
- **Age Distribution:** Histogram with risk overlay.
- **Gender Risk Analysis:** Stacked bar charts comparing risk across genders.
- **Vital Signs Correlation:** Scatter plot of Cholesterol vs. Blood Pressure.
- **BMI Analysis:** Violin plots showing BMI distribution by risk status.
- **Lifestyle Factors:** Comparison of smoking, diabetes, obesity, and alcohol consumption.
- **Age Group Vulnerability:** Risk distribution across different age brackets.
- **Overall Risk Distribution:** Pie chart of the population's risk status.

### 3. Data-Driven Insights
- **Smart Insights:** Click on any visualization to reveal detailed, dynamically generated statistical insights.
- **Modal Interface:** Clean, glassmorphism-styled popups display key statistics and interpretations.

### 4. NumPy Statistical Analysis
A dedicated analysis page powered by **NumPy** for high-performance computing:
- **Basic Statistics:** Mean, Median, Std Dev, Min/Max, and Percentiles for key metrics.
- **Correlation Matrix:** Pearson correlation coefficients between Cholesterol, Heart Rate, and BMI.
- **Risk Group Comparison:** Comparative analysis of health metrics between at-risk and healthy groups.
- **Blood Pressure Analytics:** Detailed breakdown of Systolic and Diastolic pressures.
- **Outlier Detection:** Identification of extreme values using the Interquartile Range (IQR) method.

## 🛠️ Tech Stack

- **Backend:** Python 3, Flask
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Frontend:** HTML5, CSS3 (Glassmorphism UI), JavaScript
- **Styling:** FontAwesome Icons, Custom CSS Variables

## 📂 Project Structure

```
heart-attack-risk-analysis/
├── app.py                  # Main Flask application entry point
├── requirements.txt        # Python dependencies
├── data/
│   └── dataset.csv         # Heart health dataset
├── src/                    # Source code for data processing and plotting
│   ├── __init__.py
│   ├── ahmed.py            # NumPy helper functions
│   ├── ali.py              # Pandas and NumPy data processors
│   ├── plots.py            # Matplotlib plotting classes
│   ├── aplots.py           # Additional plotting utilities
│   └── rafay.py            # Contributor module
├── static/
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   └── plots/              # Generated plot images
└── templates/              # HTML Templates
    ├── base.html           # Base template with layout
    ├── index.html          # Homepage dashboard
    ├── dataset.html        # Visualizations page
    ├── analysis.html       # NumPy analysis page
    └── about.html          # Project info and contributors
```

## ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd heart-attack-risk-analysis
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```

5.  **Access the app:**
    Open your browser and navigate to `http://127.0.0.1:5000/`

## 👥 Contributors

This project was developed by:

*   **Abdur Rafay** (01-136242-004)
*   **Ali Zafar** (01-136242-005)
*   **Ahmed Ali Khan** (01-136242-050)

## 📄 License

This project is for educational purposes.