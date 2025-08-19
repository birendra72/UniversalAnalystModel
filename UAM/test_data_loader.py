import os
from UAM import data_loader as dl
import pandas as pd

def test_load_and_preprocess_csv():
    # Create a sample CSV file
    sample_csv = 'sample_data.csv'
    data = {
        'A': [1, 1, 1, 1, 1],  # constant column
        'B': [1, 2, 3, 4, 5],
        'C': [5, 4, 3, 2, 1],
        'D': [1, 2, 3, 4, None],  # missing value
        'E': ['cat', 'dog', 'cat', 'dog', 'cat']
    }
    df_sample = pd.DataFrame(data)
    df_sample.to_csv(sample_csv, index=False)

    # Load data using data_loader
    df_loaded = dl.load_data('csv', {'filepath': sample_csv})
    print("Loaded DataFrame:")
    print(df_loaded)

    # Preprocess data
    df_processed, metadata, pca_fig = dl.preprocess_data(df_loaded)
    print("\nProcessed DataFrame:")
    print(df_processed)
    print("\nMetadata:")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    # Clean up sample file
    os.remove(sample_csv)

if __name__ == '__main__':
    test_load_and_preprocess_csv()
