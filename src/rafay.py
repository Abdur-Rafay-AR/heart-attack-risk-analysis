#Rafay's working file
import pandas as pd
import numpy as np

class DataAnalyzer:
    """
    A basic class to demonstrate Pandas and Numpy usage for data analysis.
    """
    def __init__(self, data):
        """
        Initialize with a pandas DataFrame or a path to a csv.
        """
        if isinstance(data, str):
            self.df = pd.read_csv(data)
        elif isinstance(data, pd.DataFrame):
            self.df = data
        else:
            raise ValueError("Data must be a file path or a pandas DataFrame")

    def get_basic_stats(self):
        """
        Returns descriptive statistics of the dataframe.
        """
        return self.df.describe()

    def calculate_correlation_matrix(self):
        """
        Calculates the correlation matrix using pandas.
        """
        # Select only numeric columns for correlation
        numeric_df = self.df.select_dtypes(include=[np.number])
        return numeric_df.corr()

    def get_numpy_array(self, column_name):
        """
        Converts a specific column to a numpy array.
        """
        if column_name in self.df.columns:
            return self.df[column_name].to_numpy()
        else:
            raise ValueError(f"Column {column_name} not found in DataFrame")

    def normalize_column(self, column_name):
        """
        Normalizes a column using numpy (Min-Max scaling).
        """
        arr = self.get_numpy_array(column_name)
        return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))
