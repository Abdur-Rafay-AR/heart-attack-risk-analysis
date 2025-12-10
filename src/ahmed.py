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
    
    

    
    
        
