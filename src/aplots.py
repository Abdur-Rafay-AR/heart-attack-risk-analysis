# Starting work with matplotlib
import matplotlib.pyplot as plt

class BarChart:
    def draw(self, x, y):
        plt.bar(x, y)
        plt.title("Bar Chart")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()
