from flask import Flask, render_template, send_file, abort, url_for
import os
import matplotlib
matplotlib.use('Agg') # Set backend before importing pyplot
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from src.ali import PandasProcessor

app = Flask(__name__)

# Configuration
DATA_PATH = os.path.join('data', 'dataset.csv')
STATIC_PLOTS_DIR = os.path.join('static', 'plots')
os.makedirs(STATIC_PLOTS_DIR, exist_ok=True)

def get_data():
    # Using the class from src/ali.py
    processor = PandasProcessor(DATA_PATH)
    return processor.df

@app.route("/")
def index():
    summary = {}
    try:
        df = get_data()
        summary = {
            "rows": len(df),
            "cols": len(df.columns),
            "columns": df.columns.tolist(),
        }
    except Exception as e:
        summary = {"error": f"Error loading data: {str(e)}"}
    return render_template("index.html", summary=summary)

@app.route("/dataset")
def dataset_page():
    try:
        df = get_data()
    except:
        abort(404)

    # Define available plots
    plot_names = [
        {"id": "histogram", "name": "Age Distribution"},
        {"id": "target_by_sex", "name": "Heart Attack Risk by Sex"},
        {"id": "corr_heatmap", "name": "Correlation Heatmap"},
        {"id": "scatter_chol_age", "name": "Cholesterol vs Age"},
        {"id": "boxplot_thalach", "name": "Max Heart Rate Boxplot"},
    ]

    return render_template("dataset.html", plots=plot_names)

@app.route("/plot/<plotname>")
def plot(plotname):
    df = get_data()
    plt.figure(figsize=(10, 6))
    
    # Custom color palette
    colors = ['#5A0E24', '#76153C', '#BF124D', '#800000']
    sns.set_palette(sns.color_palette(colors))
    
    filename = f"{plotname}.png"
    filepath = os.path.join(STATIC_PLOTS_DIR, filename)
    
    # Clear any existing plots
    plt.clf()
    
    try:
        if plotname == "histogram":
            sns.histplot(data=df, x='age', kde=True, color=colors[2])
            plt.title("Age Distribution")
            
        elif plotname == "target_by_sex":
            sns.countplot(data=df, x='sex', hue='output', palette=[colors[0], colors[2]])
            plt.title("Heart Attack Risk by Sex (0=Low, 1=High)")
            
        elif plotname == "corr_heatmap":
            plt.figure(figsize=(12, 10))
            sns.heatmap(df.corr(), annot=True, cmap="Reds", fmt=".2f")
            plt.title("Correlation Matrix")
            
        elif plotname == "scatter_chol_age":
            sns.scatterplot(data=df, x='age', y='chol', hue='output', palette=[colors[0], colors[2]])
            plt.title("Cholesterol vs Age")
            
        elif plotname == "boxplot_thalach":
            sns.boxplot(data=df, x='output', y='thalachh', palette=[colors[0], colors[2]])
            plt.title("Max Heart Rate vs Risk")
            
        else:
            return abort(404)
            
        plt.tight_layout()
        plt.savefig(filepath)
        plt.close()
        
        return send_file(filepath, mimetype='image/png')
        
    except Exception as e:
        plt.close()
        return str(e), 500


    if plotname not in plot_functions:
        abort(404)

    buf = plot_functions[plotname](df)
    return send_file(buf, mimetype="image/png")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
