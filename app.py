from flask import Flask, render_template, send_file, abort
from operations.loader import load_dataset
from operations import plots

app = Flask(__name__)

@app.route("/")
def index():
    summary = {}
    try:
        df = load_dataset()
        summary = {
            "rows": len(df),
            "cols": len(df.columns),
            "columns": df.columns.tolist(),
        }
    except Exception as e:
        summary = {"error": str(e)}
    return render_template("index.html", summary=summary)

@app.route("/dataset")
def dataset_page():
    try:
        df = load_dataset()
    except:
        abort(404)

    plot_names = [
        "histogram",
        "target_by_sex",
        "corr_heatmap",
        "scatter_fit",
        "boxplot",
        "density"
    ]

    return render_template("dataset.html", plots=plot_names)

@app.route("/plot/<plotname>")
def plot(plotname):
    df = load_dataset()

    plot_functions = {
        "histogram": plots.plot_histogram,
        "target_by_sex": plots.plot_target_by_sex,
        "corr_heatmap": plots.plot_corr_heatmap,
        "scatter_fit": plots.plot_scatter_with_fit,
        "boxplot": plots.plot_boxplot,
        "density": plots.plot_density,
    }

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
