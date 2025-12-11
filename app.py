from flask import Flask, render_template, send_file, abort, url_for
import os
import io
import matplotlib
matplotlib.use('Agg') # Set backend before importing pyplot
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
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

def generate_insights(df):
    """Generate insights for each plot using numpy and pandas"""
    insights = {}
    
    try:
        # 1. Age Distribution Insights
        risk_age = df[df['Heart Attack Risk'] == 1]['Age']
        no_risk_age = df[df['Heart Attack Risk'] == 0]['Age']
        
        avg_risk_age = np.mean(risk_age)
        avg_no_risk_age = np.mean(no_risk_age)
        
        insights['age_distribution'] = {
            "title": "Age & Risk Correlation",
            "stats": [
                f"Average age of at-risk patients: <strong>{avg_risk_age:.1f} years</strong>",
                f"Average age of healthy patients: <strong>{avg_no_risk_age:.1f} years</strong>",
                f"Age difference: <strong>{abs(avg_risk_age - avg_no_risk_age):.1f} years</strong>"
            ],
            "description": f"Patients at risk are on average {'older' if avg_risk_age > avg_no_risk_age else 'younger'} than those not at risk. The data suggests age is a significant factor."
        }

        # 2. Gender Risk Insights
        gender_risk = df.groupby('Sex')['Heart Attack Risk'].mean() * 100
        male_risk = gender_risk.get('Male', 0)
        female_risk = gender_risk.get('Female', 0)
        
        insights['risk_by_gender'] = {
            "title": "Gender Disparity",
            "stats": [
                f"Male Risk Rate: <strong>{male_risk:.1f}%</strong>",
                f"Female Risk Rate: <strong>{female_risk:.1f}%</strong>"
            ],
            "description": f"{'Males' if male_risk > female_risk else 'Females'} show a higher susceptibility to heart attack risk in this dataset."
        }

        # 3. Cholesterol vs BP Insights
        df['Systolic_BP'] = df['Blood Pressure'].str.split('/').str[0].astype(float)
        correlation = np.corrcoef(df['Cholesterol'], df['Systolic_BP'])[0, 1]
        avg_chol_risk = np.mean(df[df['Heart Attack Risk'] == 1]['Cholesterol'])
        
        insights['cholesterol_bp'] = {
            "title": "Vital Signs Correlation",
            "stats": [
                f"Cholesterol-BP Correlation: <strong>{correlation:.2f}</strong>",
                f"Avg Cholesterol (At Risk): <strong>{avg_chol_risk:.1f} mg/dL</strong>"
            ],
            "description": "The scatter plot reveals the relationship between cholesterol levels and blood pressure. Higher values in both metrics often correlate with increased risk."
        }

        # 4. BMI Analysis
        avg_bmi_risk = np.mean(df[df['Heart Attack Risk'] == 1]['BMI'])
        avg_bmi_healthy = np.mean(df[df['Heart Attack Risk'] == 0]['BMI'])
        
        insights['bmi_analysis'] = {
            "title": "BMI Impact",
            "stats": [
                f"Avg BMI (At Risk): <strong>{avg_bmi_risk:.1f}</strong>",
                f"Avg BMI (Healthy): <strong>{avg_bmi_healthy:.1f}</strong>"
            ],
            "description": "The box plot compares the median and spread of Body Mass Index (BMI) between risk groups, highlighting potential differences in distribution and outliers."
        }

        # 5. Lifestyle Factors
        factors = ['Smoking', 'Diabetes', 'Obesity', 'Alcohol Consumption']
        risk_factors = df[df['Heart Attack Risk'] == 1][factors].mean() * 100
        top_factor = risk_factors.idxmax()
        
        insights['lifestyle_factors'] = {
            "title": "Lifestyle Contributors",
            "stats": [f"{factor}: <strong>{val:.1f}%</strong> prevalence in at-risk group" for factor, val in risk_factors.items()],
            "description": f"<strong>{top_factor}</strong> appears to be the most prevalent lifestyle factor among patients at risk of heart attack."
        }

        # 6. Age Groups
        df['Age_Group'] = pd.cut(df['Age'], bins=[0, 30, 45, 60, 75, 100], labels=['<30', '30-45', '45-60', '60-75', '75+'])
        age_risk_rates = df.groupby('Age_Group')['Heart Attack Risk'].mean() * 100
        highest_risk_group = age_risk_rates.idxmax()
        
        insights['age_groups'] = {
            "title": "Age Group Vulnerability",
            "stats": [
                f"Highest Risk Group: <strong>{highest_risk_group}</strong>",
                f"Risk Rate in {highest_risk_group}: <strong>{age_risk_rates.max():.1f}%</strong>"
            ],
            "description": "Risk levels vary significantly across different age brackets, with specific groups showing markedly higher vulnerability."
        }

        # 7. Overall Distribution
        total_risk_rate = df['Heart Attack Risk'].mean() * 100
        
        insights['risk_distribution_pie'] = {
            "title": "Population Overview",
            "stats": [
                f"Overall Population at Risk: <strong>{total_risk_rate:.1f}%</strong>",
                f"Total Patients: <strong>{len(df)}</strong>"
            ],
            "description": "This chart provides a high-level view of the dataset's balance between at-risk and healthy individuals."
        }

        # 8. Heart Rate Line Plot
        avg_hr_by_age = df.groupby('Age')['Heart Rate'].mean()
        peak_hr_age = avg_hr_by_age.idxmax()
        
        insights['heart_rate_line'] = {
            "title": "Heart Rate Trends",
            "stats": [
                f"Peak Average Heart Rate Age: <strong>{peak_hr_age} years</strong>",
                f"Max Average Heart Rate: <strong>{avg_hr_by_age.max():.1f} bpm</strong>"
            ],
            "description": "This line plot visualizes how the average heart rate changes across different ages, highlighting potential age-related trends."
        }

        # 9. Medical Indicators Correlation Heatmap
        # Ensure Systolic_BP is available (it might be created in step 3, but good to be safe)
        if 'Systolic_BP' not in df.columns:
            df['Systolic_BP'] = df['Blood Pressure'].str.split('/').str[0].astype(float)
            
        target_cols = ['Age', 'Cholesterol', 'Heart Rate', 'BMI', 'Systolic_BP', 'Heart Attack Risk']
        # Filter for columns that actually exist
        existing_cols = [c for c in target_cols if c in df.columns]
        
        corr_matrix = df[existing_cols].corr()
        
        # Find strongest correlation with Risk (excluding Risk itself)
        if 'Heart Attack Risk' in corr_matrix.columns:
            risk_corr = corr_matrix['Heart Attack Risk'].drop('Heart Attack Risk')
            strongest_feature = risk_corr.abs().idxmax()
            strongest_val = risk_corr[strongest_feature]
        else:
            strongest_feature = "N/A"
            strongest_val = 0.0
        
        insights['correlation_heatmap'] = {
            "title": "Medical Correlations",
            "stats": [
                f"Strongest Risk Predictor: <strong>{strongest_feature}</strong>",
                f"Correlation Coefficient: <strong>{strongest_val:.2f}</strong>"
            ],
            "description": "This heatmap focuses specifically on physiological measurements (Age, BMI, BP, etc.) to identify which medical indicators have the strongest relationship with heart attack risk."
        }

        # 10. Cholesterol Area Plot
        avg_chol_by_age = df.groupby('Age')['Cholesterol'].mean()
        
        insights['cholesterol_area'] = {
            "title": "Cholesterol Accumulation",
            "stats": [
                f"Highest Avg Cholesterol: <strong>{avg_chol_by_age.max():.1f} mg/dL</strong>",
                f"Age with Highest Cholesterol: <strong>{avg_chol_by_age.idxmax()} years</strong>"
            ],
            "description": "The area plot shows the magnitude of average cholesterol levels across the age spectrum."
        }

    except Exception as e:
        print(f"Error generating insights: {e}")
        # Fallback for all keys if something fails
        for key in ['age_distribution', 'risk_by_gender', 'cholesterol_bp', 'bmi_analysis', 'lifestyle_factors', 'age_groups', 'risk_distribution_pie', 'heart_rate_line', 'correlation_heatmap', 'cholesterol_area']:
            if key not in insights:
                insights[key] = {
                    "title": "Analysis Unavailable",
                    "stats": [],
                    "description": "Could not generate insights for this visualization."
                }
                
    return insights

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
        {"id": "age_distribution", "name": "Age Distribution by Risk (Histogram)"},
        {"id": "risk_by_gender", "name": "Heart Attack Risk by Gender (Bar Chart)"},
        {"id": "cholesterol_bp", "name": "Cholesterol vs Blood Pressure (Scatter Plot)"},
        {"id": "bmi_analysis", "name": "BMI Distribution by Risk (Box Plot)"},
        {"id": "lifestyle_factors", "name": "Lifestyle Risk Factors (Bar Chart)"},
        {"id": "age_groups", "name": "Risk Distribution Across Age Groups (Stacked Bar)"},
        {"id": "risk_distribution_pie", "name": "Overall Risk Distribution (Pie Chart)"},
        {"id": "heart_rate_line", "name": "Avg Heart Rate by Age (Line Plot)"},
        {"id": "correlation_heatmap", "name": "Feature Correlation (Heatmap)"},
        {"id": "cholesterol_area", "name": "Cholesterol Levels by Age (Area Plot)"},
    ]

    # Generate insights
    insights = generate_insights(df)
    
    # Attach insights to plot objects
    for plot in plot_names:
        if plot['id'] in insights:
            plot['insight'] = insights[plot['id']]

    return render_template("dataset.html", plots=plot_names)

@app.route("/analysis")
def analysis_page():
    try:
        df = get_data()
        
        # Basic Statistics using NumPy
        # We'll analyze Age, Cholesterol, Heart Rate, and BMI
        columns_to_analyze = {
            'Age': df['Age'].values,
            'Cholesterol': df['Cholesterol'].values,
            'Heart Rate': df['Heart Rate'].values,
            'BMI': df['BMI'].values
        }
        
        basic_stats = {}
        for name, data in columns_to_analyze.items():
            q25, q75 = np.percentile(data, [25, 75])
            basic_stats[name] = {
                'mean': np.mean(data),
                'median': np.median(data),
                'std': np.std(data),
                'min': np.min(data),
                'max': np.max(data),
                'q25': q25,
                'q75': q75
            }
            
        # Correlation Analysis using NumPy
        # Extracting arrays
        chol = df['Cholesterol'].values
        hr = df['Heart Rate'].values
        bmi = df['BMI'].values
        
        # Calculate correlations
        correlations = {
            'chol_hr': np.corrcoef(chol, hr)[0, 1],
            'chol_bmi': np.corrcoef(chol, bmi)[0, 1],
            'hr_bmi': np.corrcoef(hr, bmi)[0, 1]
        }

        # Advanced: Blood Pressure Analysis (NumPy)
        # Split string column and convert to numpy array
        bp_series = df['Blood Pressure'].str.split('/')
        systolic = np.array([float(x[0]) for x in bp_series])
        diastolic = np.array([float(x[1]) for x in bp_series])
        
        bp_stats = {
            'systolic_mean': np.mean(systolic),
            'systolic_max': np.max(systolic),
            'diastolic_mean': np.mean(diastolic),
            'diastolic_max': np.max(diastolic),
            'pulse_pressure_mean': np.mean(systolic - diastolic) # Pulse pressure = Sys - Dia
        }

        # Advanced: Outlier Detection using IQR (NumPy)
        outlier_stats = {}
        for name, data in {'Cholesterol': chol, 'BMI': bmi, 'Heart Rate': hr}.items():
            q1, q3 = np.percentile(data, [25, 75])
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            # Boolean indexing to find outliers
            outliers_count = np.sum((data < lower_bound) | (data > upper_bound))
            outlier_stats[name] = {
                'count': int(outliers_count),
                'lower': lower_bound,
                'upper': upper_bound
            }
        
        # Risk Group Analysis using Boolean Indexing
        risk_mask = df['Heart Attack Risk'].values == 1
        no_risk_mask = df['Heart Attack Risk'].values == 0
        
        risk_stats = {
            'risk_age_mean': np.mean(df['Age'].values[risk_mask]),
            'no_risk_age_mean': np.mean(df['Age'].values[no_risk_mask]),
            'risk_chol_mean': np.mean(df['Cholesterol'].values[risk_mask]),
            'no_risk_chol_mean': np.mean(df['Cholesterol'].values[no_risk_mask])
        }
        
        return render_template("analysis.html", 
                             basic_stats=basic_stats, 
                             correlations=correlations, 
                             risk_stats=risk_stats,
                             bp_stats=bp_stats,
                             outlier_stats=outlier_stats)
                             
    except Exception as e:
        return f"Error performing analysis: {str(e)}", 500

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
        if plotname in ["cholesterol_bp", "bmi_analysis", "lifestyle_factors", "risk_distribution_pie", "correlation_heatmap"]:
            figsize = (8, 6)
            
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
            # Box plot for BMI distribution
            sns.boxplot(data=df, x='Heart Attack Risk', y='BMI', 
                          palette=risk_colors, ax=ax)
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
            risk_counts = df['Heart Attack Risk'].value_counts().sort_index()
            
            # Dynamic configuration based on available data
            labels = []
            pie_colors = []
            explode = []
            
            for val in risk_counts.index:
                if val == 0:
                    labels.append('No Risk')
                    pie_colors.append(colors[0])
                else:
                    labels.append('At Risk')
                    pie_colors.append(colors[2])
                explode.append(0.05)

            # Create pie chart with improved text positioning
            wedges, texts, autotexts = ax.pie(
                risk_counts, 
                labels=labels, 
                autopct='%1.1f%%', 
                startangle=90, 
                colors=pie_colors, 
                explode=explode,
                textprops={'fontsize': 14, 'color': 'white', 'fontweight': 'bold'},
                pctdistance=0.80  # Move percentage labels closer to edge
            )
            
            ax.set_title("Overall Heart Attack Risk Distribution", 
                        fontsize=18, fontweight='bold', color='white', pad=20)
            
            # Add count labels with better positioning
            for i, (wedge, count) in enumerate(zip(wedges, risk_counts)):
                angle = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
                x = wedge.r * 0.5 * np.cos(np.radians(angle))  # Position at 50% radius
                y = wedge.r * 0.5 * np.sin(np.radians(angle))
                ax.text(x, y, f'n={count}', 
                        ha='center', va='center', 
                        fontsize=12, color='white', 
                        weight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.3, edgecolor='none'))
            
            # Style the percentage text for better readability
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(13)
                autotext.set_weight('bold')
            
            # Style the label text
            for text in texts:
                text.set_color('white')
                text.set_fontsize(15)
                text.set_weight('bold')
            
            # Ensure aspect ratio is equal so pie is drawn as a circle
            ax.axis('equal')
            
        elif plotname == "heart_rate_line":
            # Line Plot: Average Heart Rate by Age
            avg_hr = df.groupby('Age')['Heart Rate'].mean()
            avg_hr.plot(kind='line', color=colors[2], ax=ax, linewidth=2, marker='o', markersize=4)
            ax.set_title("Average Heart Rate by Age", fontsize=18, fontweight='bold', color='white', pad=20)
            ax.set_xlabel('Age (years)', fontsize=13, color='#e0e0e0')
            ax.set_ylabel('Average Heart Rate (bpm)', fontsize=13, color='#e0e0e0')
            ax.grid(True, alpha=0.2)

        elif plotname == "correlation_heatmap":
            # Heatmap: Medical Indicators Correlation
            # Create Systolic BP if not exists
            if 'Systolic_BP' not in df.columns:
                df['Systolic_BP'] = df['Blood Pressure'].str.split('/').str[0].astype(float)
            
            cols_to_plot = ['Age', 'Cholesterol', 'Heart Rate', 'BMI', 'Systolic_BP', 'Heart Attack Risk']
            # Filter only existing columns
            cols_to_plot = [c for c in cols_to_plot if c in df.columns]
            
            corr = df[cols_to_plot].corr()
            
            sns.heatmap(corr, annot=True, fmt=".2f", cmap='RdYlBu_r', ax=ax, 
                       cbar_kws={'label': 'Correlation Coefficient'}, vmin=-1, vmax=1)
            ax.set_title("Medical Indicators Correlation Matrix", fontsize=18, fontweight='bold', color='white', pad=20)
            # Fix for heatmap labels being cut off
            plt.xticks(rotation=45, ha='right')
            plt.yticks(rotation=0)

        elif plotname == "cholesterol_area":
            # Area Plot: Average Cholesterol by Age
            avg_chol = df.groupby('Age')['Cholesterol'].mean()
            ax.fill_between(avg_chol.index, avg_chol.values, color=colors[2], alpha=0.4)
            ax.plot(avg_chol.index, avg_chol.values, color=colors[3], linewidth=2)
            ax.set_title("Average Cholesterol Levels by Age", fontsize=18, fontweight='bold', color='white', pad=20)
            ax.set_xlabel('Age (years)', fontsize=13, color='#e0e0e0')
            ax.set_ylabel('Cholesterol (mg/dL)', fontsize=13, color='#e0e0e0')
            ax.grid(True, alpha=0.2)

        else:
            plt.close(fig)
            return abort(404)
        
        # Apply consistent dark theme styling (skip for pie charts and heatmaps)
        if plotname not in ["risk_distribution_pie", "correlation_heatmap"]:
            ax.set_facecolor('#0a0a0a')
            ax.tick_params(colors='#e0e0e0', labelsize=10)
            ax.spines['bottom'].set_color('#e0e0e0')
            ax.spines['left'].set_color('#e0e0e0')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(alpha=0.15, linestyle='--', linewidth=0.5)
        
        # Adjust layout
        if plotname != "risk_distribution_pie":
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
