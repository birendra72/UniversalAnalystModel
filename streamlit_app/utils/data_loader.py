import pandas as pd
import numpy as np
from sklearn.feature_selection import VarianceThreshold

def load_data(uploaded_file):
    """Load data from uploaded file"""
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Unsupported file format")
    return df

def preprocess_data(df, remove_constant=True, remove_correlated=True):
    """Preprocess data based on selected options"""
    if remove_constant:
        constant_filter = VarianceThreshold(threshold=0)
        numeric_df = df.select_dtypes(include=np.number)
        constant_filter.fit(numeric_df)
        constant_columns = [col for col in numeric_df.columns if col not in numeric_df.columns[constant_filter.get_support()]]
        df = df.drop(columns=constant_columns)
    
    if remove_correlated:
        corr_matrix = df.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        to_drop = [column for column in upper.columns if any(upper[column] > 0.95)]
        df = df.drop(columns=to_drop)
    
    return df
