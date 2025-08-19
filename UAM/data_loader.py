import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sqlalchemy import create_engine
import json

def load_data(source_type, source_config):
    """
    Load data from various sources into a pandas DataFrame.

    Parameters:
    - source_type: str, one of ['csv', 'xlsx', 'json', 'sqlite', 'mysql', 'postgresql']
    - source_config: dict, configuration for the source
        For files: {'filepath': 'path/to/file'}
        For databases: {'connection_string': 'db_connection_string', 'query': 'SELECT ...'}

    Returns:
    - df: pandas DataFrame
    """
    print(f"Loading data from source type: {source_type}")
    df = None
    if source_type == 'csv':
        filepath = source_config.get('filepath')
        df = pd.read_csv(filepath)
    elif source_type == 'xlsx':
        filepath = source_config.get('filepath')
        df = pd.read_excel(filepath, engine='openpyxl')
    elif source_type == 'json':
        filepath = source_config.get('filepath')
        df = pd.read_json(filepath)
    elif source_type in ['sqlite', 'mysql', 'postgresql']:
        connection_string = source_config.get('connection_string')
        query = source_config.get('query')
        engine = create_engine(connection_string)
        df = pd.read_sql(query, engine)
    else:
        raise ValueError(f"Unsupported source_type: {source_type}")

    print(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns.")
    return df

def preprocess_data(df, corr_threshold=0.95, missing_threshold=0.6, pca_variance=0.95):
    """
    Preprocess the DataFrame by removing constant and redundant features,
    handling missing values, auto-detecting column types, and applying PCA.

    Parameters:
    - df: pandas DataFrame
    - corr_threshold: float, correlation threshold to remove redundant features
    - missing_threshold: float, threshold to drop columns with missing values above this fraction
    - pca_variance: float, variance ratio to keep in PCA

    Returns:
    - df_processed: pandas DataFrame after preprocessing (PCA applied if triggered)
    - metadata: dict with preprocessing summary and dataset profile
    - pca_fig: matplotlib Figure object of explained variance plot (or None if PCA not applied)
    """
    metadata = {}
    original_shape = df.shape
    print(f"Original data shape: {original_shape}")

    # 1. Remove constant features
    constant_cols = [col for col in df.columns if df[col].nunique(dropna=False) == 1]
    df = df.drop(columns=constant_cols)
    print(f"Removed {len(constant_cols)} constant columns: {constant_cols}")

    # 2. Remove redundant (highly correlated) features
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr().abs()
    upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > corr_threshold)]
    df = df.drop(columns=to_drop)
    print(f"Dropped {len(to_drop)} highly correlated columns: {to_drop}")

    # 3. Handle missing values
    missing_percent = df.isnull().mean()
    missing_report = missing_percent[missing_percent > 0].sort_values(ascending=False)
    for col, pct in missing_report.items():
        print(f"Column '{col}' has {pct:.2%} missing values")
    drop_missing_cols = missing_percent[missing_percent > missing_threshold].index.tolist()
    df = df.drop(columns=drop_missing_cols)
    print(f"Dropped {len(drop_missing_cols)} columns with >{missing_threshold*100:.0f}% missing values: {drop_missing_cols}")

    # Optionally, fill or flag minor missing entries - here we fill numeric with median, categorical with mode
    minor_missing_cols = missing_percent[(missing_percent > 0) & (missing_percent <= missing_threshold)].index.tolist()
    for col in minor_missing_cols:
        if df[col].dtype in [np.float64, np.int64]:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"Filled missing values in numeric column '{col}' with median: {median_val}")
        else:
            mode_val = df[col].mode(dropna=True)
            if not mode_val.empty:
                mode_val = mode_val[0]
                df[col] = df[col].fillna(mode_val)
                print(f"Filled missing values in categorical column '{col}' with mode: {mode_val}")
            else:
                df[col] = df[col].fillna('Missing')
                print(f"Filled missing values in categorical column '{col}' with 'Missing'")

    # 4. Auto-detect column types
    col_types = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            col_types[col] = 'numerical'
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            col_types[col] = 'datetime'
        elif df[col].nunique() == df.shape[0]:
            col_types[col] = 'id-like'
        else:
            col_types[col] = 'categorical'
    print(f"Detected column types: { {k: v for k, v in list(col_types.items())[:10]} } ...")

    # 5. Dimensionality Reduction using PCA if features > 10
    pca_fig = None
    numeric_cols = [col for col, typ in col_types.items() if typ == 'numerical']
    df_numeric = df[numeric_cols].copy()
    if df_numeric.shape[1] > 10:
        print(f"Applying PCA on {df_numeric.shape[1]} numerical features")
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df_numeric)
        pca = PCA(n_components=pca_variance, svd_solver='full')
        pca_data = pca.fit_transform(scaled_data)
        explained_var = np.cumsum(pca.explained_variance_ratio_) * 100
        n_components = pca_data.shape[1]
        print(f"PCA reduced features to {n_components} components explaining {explained_var[-1]:.2f}% variance")

        # Create explained variance plot
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.lineplot(x=range(1, n_components + 1), y=explained_var, marker='o', ax=ax)
        ax.set_xlabel('Number of Components')
        ax.set_ylabel('Cumulative Explained Variance (%)')
        ax.set_title('PCA Explained Variance')
        ax.grid(True)
        pca_fig = fig

        # Replace numerical columns with PCA components
        pca_cols = [f'PCA_{i+1}' for i in range(n_components)]
        df_pca = pd.DataFrame(pca_data, columns=pca_cols, index=df.index)

        # Keep non-numerical columns as is
        non_numeric_cols = [col for col in df.columns if col not in numeric_cols]
        df_processed = pd.concat([df_pca, df[non_numeric_cols]], axis=1)
    else:
        print(f"PCA not applied, number of numerical features ({df_numeric.shape[1]}) <= 10")
        df_processed = df

    final_shape = df_processed.shape
    print(f"Final data shape after preprocessing: {final_shape}")

    metadata['original_shape'] = original_shape
    metadata['final_shape'] = final_shape
    metadata['constant_columns_removed'] = constant_cols
    metadata['highly_correlated_columns_removed'] = to_drop
    metadata['columns_dropped_missing'] = drop_missing_cols
    metadata['column_types'] = col_types
    metadata['pca_applied'] = df_numeric.shape[1] > 10
    if df_numeric.shape[1] > 10:
        metadata['pca_n_components'] = n_components
        metadata['pca_explained_variance'] = explained_var[-1]

    return df_processed, metadata, pca_fig
