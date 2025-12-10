#Ahmed's working file :)
import numpy as np

class NumPyfunc:
    def __init__(self, d):
        self.d = d
        self.a = d.select_dtypes(include=[np.number]).to_numpy()
    def get_mean(self):
        return np.mean(self.a, axis=0)     # axis 0 is Row , this function gets the mean
    
    
        
