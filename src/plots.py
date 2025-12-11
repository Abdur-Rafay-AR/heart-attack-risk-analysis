import matplotlib.pyplot as plt

class LinePlotter:
    def __init__(self, df):
        self.df = df

    def line_plot(self, column):
        plt.plot(self.df[column])
        plt.title(f"{column} Line Plot")
        plt.xlabel("Index")
        plt.ylabel(column)
        plt.show()
    
class ScatterPlotter:
    def __init__(self, df):
        self.df = df

    def scatter_plot(self, x_col, y_col):
        plt.scatter(self.df[x_col], self.df[y_col])
        plt.title(f"{x_col} vs {y_col} Scatter Plot")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.show()

class HistogramPlotter:
    def __init__(self, df):
        self.df = df

    def histogram(self, column):
        plt.hist(self.df[column])
        plt.title(f"{column} Histogram")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.show()
