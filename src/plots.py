#file for plotting using matplotlib

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
