# Starting work with matplotlib
import matplotlib.pyplot as plt

class BarChart:
    def draw(self, x, y):
        plt.bar(x, y)
        plt.title("Bar Chart")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()
        
import matplotlib.pyplot as plt

class BoxPlot:
    def draw(self, data):
        plt.boxplot(data)
        plt.title("Box Plot")
        plt.ylabel("Values")
        plt.show()
