#Ali's working filei
import pandas as pd
import numpy as np
class PandasProcessor:
    
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)