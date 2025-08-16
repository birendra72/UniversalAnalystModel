import sys
import data_loader as dl
import eda_engine as eda
import insight_extractor as ie
import modeling as model
import os
from nl_query_interface import NaturalLanguageQueryInterface
import report_generator as rg

def prompt_data_source():
    print("Select data source type:")
    print("1. CSV")
    print("2. XLSX")
    print("3. JSON")
    print("4. SQLite")
    print("5. MySQL")
    print("6. PostgreSQL")
    choice = input("Enter choice number (1-6): ").strip()
    source_type_map = {
        '1': 'csv',
        '2': 'xlsx',
        '3': 'json',
        '4': 'sqlite',
        '5': 'mysql',
        '6': 'postgresql'
    }
    source_type = source_type_map.get(choice)
    if not source_type:
        print("Invalid choice. Exiting.")
        sys.exit(1)
    return source_type

def prompt_source_config(source_type):
    config = {}
    if source_type in ['csv', 'xlsx', 'json']:
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            root.attributes('-topmost', True)  # Make the dialog appear above all windows
            filetypes = {
                'csv': [('CSV files', '*.csv')],
                'xlsx': [('Excel files', '*.xlsx')],
                'json': [('JSON files', '*.json')]
            }
            filepath = filedialog.askopenfilename(title=f"Select {source_type.upper()} file", filetypes=filetypes.get(source_type, [('All files', '*.*')]))
            if not filepath:
                print("No file selected. Exiting.")
                sys.exit(1)
            config['filepath'] = filepath
        except Exception as e:
            print(f"Could not open file dialog due to: {e}")
            filepath = input(f"Enter the file path for the {source_type.upper()} file: ").strip()
            if not filepath:
                print("No file path entered. Exiting.")
                sys.exit(1)
            config['filepath'] = filepath
    else:
        connection_string = input(f"Enter the connection string for the {source_type.upper()} database: ").strip()
        query = input("Enter the SQL query to fetch data: ").strip()
        config['connection_string'] = connection_string
        config['query'] = query
    return config

def main():
    while True:
        print("Universal Analyst Model - Step 1: Data Input + Adaptive Feature Handling")
        source_type = prompt_data_source()
        source_config = prompt_source_config(source_type)

        try:
            df = dl.load_data(source_type, source_config)
        except Exception as e:
            print(f"Error loading data: {e}")
            continue

        try:
            df_processed, metadata, pca_fig = dl.preprocess_data(df)
        except Exception as e:
            print(f"Error during preprocessing: {e}")
            continue

        print("\nPreprocessing Summary:")
        for key, value in metadata.items():
            print(f"{key}: {value}")

        if pca_fig:
            try:
                import matplotlib.pyplot as plt
                plt.show()
            except ImportError:
                print("matplotlib not installed, cannot show PCA plot.")

        print("\nUniversal Analyst Model - Step 2: Automated EDA & Insight Extraction")
        try:
            dataset_name = None
            if source_type in ['csv', 'xlsx', 'json']:
                dataset_name = os.path.splitext(os.path.basename(source_config.get('filepath', '')))[0]
            save_path = os.path.join("reports", dataset_name) if dataset_name else "reports/"
            eda.run_full_eda(df_processed, save_path=save_path)
        except Exception as e:
            print(f"Error during EDA: {e}")
            continue

        print("\nUniversal Analyst Model - Step 3: Insight Extraction and Data Understanding")
        try:
            insight_report_dir = os.path.join("reports", dataset_name) if dataset_name else "reports/general"
            os.makedirs(insight_report_dir, exist_ok=True)
            insight_report_path = os.path.join(insight_report_dir, "insight_report.md")
            ie.run_insight_extraction(df_processed, output_path=insight_report_path)
        except Exception as e:
            print(f"Error during Insight Extraction: {e}")
            continue

        print("\nUniversal Analyst Model - Step 4: Intelligent Modeling and Prediction")
        try:
            model_report_dir = os.path.join("reports", dataset_name) if dataset_name else "reports/general"
            os.makedirs(model_report_dir, exist_ok=True)
            model_report_path = os.path.join(model_report_dir, "model_report.md")
            model_dir = os.path.join("models", dataset_name) if dataset_name else "models/general"
            model.run_modeling(df_processed, output_dir=model_report_dir, model_dir=model_dir)
        except Exception as e:
            print(f"Error during Modeling: {e}")
            continue

        print("\nUniversal Analyst Model - Step 5: Automated Report Generation and Export")
        try:
            # import report_generator as rg
            eda_summary_path = os.path.join("reports", dataset_name, "eda_report.md") if dataset_name else os.path.join("reports", "general", "eda_report.md")
            insight_report_path = os.path.join("reports", dataset_name, "insight_report.md") if dataset_name else os.path.join("reports", "general", "insight_report.md")
            model_report_path = os.path.join("reports", dataset_name, "model_report.md") if dataset_name else os.path.join("reports", "general", "model_report.md")
            rg.generate_full_report(
                dataset_name=dataset_name or "general",
                step1_metadata=metadata,
                eda_summary_path=eda_summary_path,
                insight_report_path=insight_report_path,
                model_report_path=model_report_path,
                output_dir=os.path.join("reports", dataset_name) if dataset_name else "reports/general",
                output_formats=["md", "pdf"]
            )
        except Exception as e:
            print(f"Error during Report Generation: {e}")
            continue

        print("\nUniversal Analyst Model - Step 6: Natural Language Query Interface")
        try:
            openai_api_key = os.getenv('OPENAI_API_KEY')
            # os.getenv('GEMINI_API_KEY') or 
            if not openai_api_key:
                raise ValueError("OpenAI API key not provided. Set GEMINI_API_KEY or OPENAI_API_KEY environment variable.")
            nlq = NaturalLanguageQueryInterface(df,openai_api_key)
            print("Enter your natural language queries about the dataset. Type 'exit' to quit.")
            while True:
                query = input("Query> ")
                if query.lower() in ['exit', 'quit']:
                    break
                try:
                    result = nlq.ask(query)
                    print(result)
                except Exception as e:
                    print(f"Error: {e}")
        except Exception as e:
            print(f"Error during Natural Language Query Interface: {e}")
            continue

        cont = input("\nDo you want to analyze another dataset? (y/n): ").strip().lower()
        if cont != 'y':
            print("Exiting Universal Analyst Model CLI.")
            break

if __name__ == '__main__':
    main()
