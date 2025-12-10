#Ahmed's working file :)
import numpy as np
import pandas as pd

class NumPyfunc:
    def __init__(self, d):
        self.d = d
        self.a = d.select_dtypes(include=[np.number]).to_numpy()
    
    def get_mean(self):
        return np.mean(self.a, axis=0)     
    
    def get_min(self):
        return np.min(self.a, axis=0)     
    
    def get_max(self):
        return np.max(self.a, axis=0)
    
    def get_std(self):
        return np.std(self.a, axis=0)
    
    def get_col_values(self, c):
        return self.d[c].to_numpy()
    
    def add_arrays(self, x, y):
        return np.add(x, y)
    
    def mul_arrays(self, x, y):
        return np.multiply(x, y)
    
class PanFunc:
    def __init__(self, d):
        self.d = d
    
    def head_rows(self, n):
        return self.d.head(n)
    
    def col_mean(self, c):
        return self.d[c].mean()
    
    def col_sum(self, c):
        return self.d[c].sum()
    
    def col_unique(self, c):
        return self.d[c].unique()
    
    def filter_eq(self, c, v):
        return self.d[self.d[c] == v]
    
    def sort_by(self, c):
        return self.d.sort_values(by=c)
    

    
    
        
