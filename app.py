from flask import Flask, render_template, send_file, abort, url_for
import os
import io
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
            "sample_data": df.head(5).to_dict(orient='records')
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
        {"id": "age_distribution", "name": "Age Distribution by Risk"},
        {"id": "risk_by_gender", "name": "Heart Attack Risk by Gender"},
        {"id": "cholesterol_bp", "name": "Cholesterol vs Blood Pressure"},
        {"id": "bmi_analysis", "name": "BMI Distribution by Risk"},
        {"id": "lifestyle_factors", "name": "Lifestyle Risk Factors"},
        {"id": "age_groups", "name": "Risk Distribution Across Age Groups"},
        {"id": "risk_distribution_pie", "name": "Overall Risk Distribution"},
    ]

    return render_template("dataset.html", plots=plot_names)

@app.route("/plot/<plotname>")
def plot(plotname):
    try:
        df = get_data()
        
        # Custom color palette
        colors = ['#5A0E24', '#76153C', '#BF124D', '#800000']
        risk_colors = [colors[0], colors[2]]  # Low risk, High risk
        
        # Set dark theme for plots
        plt.style.use('dark_background')
        sns.set_palette(sns.color_palette(colors))
        
        # Create figure based on plot type
        figsize = (12, 7)
        if plotname in ["cholesterol_bp", "bmi_analysis", "lifestyle_factors"]:
            figsize = (8, 5)
            
        fig, ax = plt.subplots(figsize=figsize, facecolor='#1a1a1a')
        
        # Generate specific plots
        if plotname == "age_distribution":
            # Age distribution with risk overlay
            sns.histplot(data=df, x='Age', hue='Heart Attack Risk', 
                        bins=30, kde=True, palette=risk_colors, alpha=0.6, ax=ax)
            ax.set_title("Age Distribution by Heart Attack Risk", fontsize=18, fontweight='bold', color='white', pad=20)
            ax.set_xlabel('Age (years)', fontsize=13, color='#e0e0e0')
            ax.set_ylabel('Frequency', fontsize=13, color='#e0e0e0')
            ax.legend(title='Risk Level', labels=['No Risk', 'At Risk'], fontsize=10)
            
        elif plotname == "risk_by_gender":
            # Stacked bar chart for gender and risk
            risk_gender = df.groupby(['Sex', 'Heart Attack Risk']).size().unstack(fill_value=0)
            risk_gender.plot(kind='bar', stacked=False, color=risk_colors, ax=ax, width=0.6)
            ax.set_title("Heart Attack Risk by Gender", fontsize=18, fontweight='bold', color='white', pad=20)
            ax.set_xlabel('Gender', fontsize=13, color='#e0e0e0')
            ax.set_ylabel('Number of Patients', fontsize=13, color='#e0e0e0')
            ax.legend(title='Risk Status', labels=['No Risk', 'At Risk'], fontsize=10)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
            
        elif plotname == "cholesterol_bp":
            # Extract systolic BP (first number)
            df['Systolic_BP'] = df['Blood Pressure'].str.split('/').str[0].astype(float)
            # Scatter plot with size based on age
            scatter = ax.scatter(df['Cholesterol'], df['Systolic_BP'], 
                               c=df['Heart Attack Risk'], s=df['Age']*2, 
                               alpha=0.6, cmap='RdYlBu_r', edgecolors='white', linewidth=0.5)
            ax.set_title("Cholesterol vs Blood Pressure (size = age)", fontsize=18, fontweight='bold', color='white', pad=20)
            ax.set_xlabel('Cholesterol (mg/dL)', fontsize=13, color='#e0e0e0')
            ax.set_ylabel('Systolic Blood Pressure (mmHg)', fontsize=13, color='#e0e0e0')
            # Set axis limits based on data range with padding
            ax.set_xlim(df['Cholesterol'].min() - 20, df['Cholesterol'].max() + 20)
            ax.set_ylim(df['Systolic_BP'].min() - 10, df['Systolic_BP'].max() + 10)
            cbar = plt.colorbar(scatter, ax=ax)
            cbar.set_label('Heart Attack Risk', fontsize=11, color='#e0e0e0')
            cbar.ax.yaxis.set_tick_params(color='#e0e0e0')
            plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#e0e0e0')
            
        elif plotname == "bmi_analysis":
            # Violin plot for BMI distribution
            sns.violinplot(data=df, x='Heart Attack Risk', y='BMI', 
                          palette=risk_colors, ax=ax, inner='quartile')
            ax.set_title("BMI Distribution by Risk Status", fontsize=18, fontweight='bold', color='white', pad=20)
            ax.set_xlabel('Heart Attack Risk', fontsize=13, color='#e0e0e0')
            ax.set_ylabel('BMI (Body Mass Index)', fontsize=13, color='#e0e0e0')
            ax.set_xticklabels(['No Risk', 'At Risk'])
            # Add mean lines
            means = df.groupby('Heart Attack Risk')['BMI'].mean()
            for i, mean in enumerate(means):
                ax.hlines(mean, i-0.4, i+0.4, colors='yellow', linestyle='--', linewidth=2, label=f'Mean: {mean:.1f}' if i==0 else '')
            
        elif plotname == "lifestyle_factors":
            # Multiple lifestyle factors comparison
            lifestyle_data = df[['Diabetes', 'Smoking', 'Obesity', 'Alcohol Consumption', 'Heart Attack Risk']]
            risk_lifestyle = lifestyle_data.groupby('Heart Attack Risk')[['Diabetes', 'Smoking', 'Obesity', 'Alcohol Consumption']].mean()
            risk_lifestyle = risk_lifestyle.T
            risk_lifestyle.plot(kind='barh', color=risk_colors, ax=ax, width=0.7)
            ax.set_title("Lifestyle Risk Factors Comparison", fontsize=18, fontweight='bold', color='white', pad=20)
            ax.set_xlabel('Proportion of Patients', fontsize=13, color='#e0e0e0')
            ax.set_ylabel('Risk Factor', fontsize=13, color='#e0e0e0')
            ax.legend(title='Risk Status', labels=['No Risk', 'At Risk'], fontsize=10)
            ax.set_xlim(0, 1)
            
        elif plotname == "age_groups":
            # Age groups risk distribution
            df['Age_Group'] = pd.cut(df['Age'], bins=[0, 30, 45, 60, 75, 100], 
                                     labels=['<30', '30-45', '45-60', '60-75', '75+'])
            age_risk = df.groupby(['Age_Group', 'Heart Attack Risk']).size().unstack(fill_value=0)
            age_risk_pct = age_risk.div(age_risk.sum(axis=1), axis=0) * 100
            age_risk_pct.plot(kind='bar', stacked=True, color=risk_colors, ax=ax, width=0.7)
            ax.set_title("Risk Distribution Across Age Groups", fontsize=18, fontweight='bold', color='white', pad=20)
            ax.set_xlabel('Age Group', fontsize=13, color='#e0e0e0')
            ax.set_ylabel('Percentage (%)', fontsize=13, color='#e0e0e0')
            ax.legend(title='Risk Status', labels=['No Risk', 'At Risk'], fontsize=10)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
            ax.set_ylim(0, 100)
            
        elif plotname == "risk_distribution_pie":
            # Pie chart for overall risk distribution
            risk_counts = df['Heart Attack Risk'].value_counts()
            colors_pie = [colors[0], colors[2]]
            explode = (0.05, 0.05)
            wedges, texts, autotexts = ax.pie(risk_counts, labels=['No Risk', 'At Risk'], 
                                               autopct='%1.1f%%', startangle=90, 
                                               colors=colors_pie, explode=explode,
                                               textprops={'fontsize': 14, 'color': 'white', 'fontweight': 'bold'})
            ax.set_title("Overall Heart Attack Risk Distribution", fontsize=18, fontweight='bold', color='white', pad=20)
            # Add count labels
            for i, (wedge, count) in enumerate(zip(wedges, risk_counts)):
                angle = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
                x = wedge.r * 0.7 * plt.cos(plt.radians(angle))
                y = wedge.r * 0.7 * plt.sin(plt.radians(angle))
                ax.text(x, y, f'n={count}', ha='center', va='center', fontsize=11, color='white', weight='bold')
            
        else:
            plt.close(fig)
            return abort(404)
        
        # Apply consistent dark theme styling
        ax.set_facecolor('#0a0a0a')
        ax.tick_params(colors='#e0e0e0', labelsize=10)
        ax.spines['bottom'].set_color('#e0e0e0')
        ax.spines['left'].set_color('#e0e0e0')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(alpha=0.15, linestyle='--', linewidth=0.5)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save to file in static/plots directory
        filename = f"{plotname}.png"
        filepath = os.path.join(STATIC_PLOTS_DIR, filename)
        fig.savefig(filepath, format='png', facecolor='#1a1a1a', edgecolor='none', 
                   dpi=120, bbox_inches='tight', metadata={})
        
        # Also save to memory buffer for immediate serving
        img_bytes = io.BytesIO()
        fig.savefig(img_bytes, format='png', facecolor='#1a1a1a', edgecolor='none', 
                   dpi=120, bbox_inches='tight', metadata={})
        img_bytes.seek(0)
        
        plt.close(fig)
        
        return send_file(img_bytes, mimetype='image/png', as_attachment=False)
        
    except Exception as e:
        if 'fig' in locals():
            plt.close(fig)
        return f"Error generating plot: {str(e)}", 500

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
