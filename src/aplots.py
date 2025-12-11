# Starting work with matplotlib
import matplotlib.pyplot as plt

class BarChart:
    def draw(self, x, y):
        plt.bar(x, y)
        plt.title("Bar Chart")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()

class BoxPlot:
    def draw(self, data):
        plt.boxplot(data)
        plt.title("Box Plot")
        plt.ylabel("Values")
        plt.show()

class PieChart:
    def draw(self, data):
        plt.pie(data, autopct="%1.1f%%")
        plt.title("Pie Chart")
        plt.show()

class LinePlot:
    def draw(self, y):
        plt.plot(y)
        plt.title("Line Plot")
        plt.ylabel("Values")
        plt.xlabel("Index")
        plt.show()

class Heatmap:
    def draw(self, data):
        plt.imshow(data, aspect="auto")
        plt.colorbar()
        plt.title("Correlation Heatmap")
        plt.show()        