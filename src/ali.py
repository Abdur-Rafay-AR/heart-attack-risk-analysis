#Ali's working filei
import pandas as pd
import numpy as np

class PandasProcessor:
    
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)

    def column_mean(self):
        return self.df.mean(numeric_only=True)
    
    def column_sum(self):
        return self.df.sum(numeric_only=True)
    
    def describe_data(self):
        return self.df.describe()
