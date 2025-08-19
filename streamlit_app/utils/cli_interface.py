import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from UAM import data_loader, eda_engine, modeling, nl_query_interface, report_generator
from  UAM import insight_extractor
from UAM.nl_query_interface import NaturalLanguageQueryInterface

def load_data(source_type, source_config):
    return data_loader.load_data(source_type, source_config)

def preprocess_data(df, **kwargs):
    return data_loader.preprocess_data(df, **kwargs)

def run_eda(df, save_path="eda_outputs/"):
    eda_engine.run_full_eda(df, save_path=save_path)

def run_insight_extraction_local(df, output_path):
    return insight_extractor.run_insight_extraction(df, output_path)

def run_modeling(df, provided_target=None, output_dir="reports", model_dir="models"):
    return modeling.run_modeling(df, provided_target, output_dir, model_dir)

def generate_report(dataset_name, step1_metadata, eda_summary_path, insight_report_path, model_report_path=None, output_dir="reports", output_formats=["md", "pdf"]):
    report_generator.generate_full_report(
        dataset_name=dataset_name,
        step1_metadata=step1_metadata,
        eda_summary_path=eda_summary_path,
        insight_report_path=insight_report_path,
        model_report_path=model_report_path,
        output_dir=output_dir,
        output_formats=output_formats
    )

def create_nlq_interface(df, openai_api_key, model_name="gpt-3.5-turbo"):
    return NaturalLanguageQueryInterface(df, openai_api_key, model_name)

def run_insight_extraction(df, output_path="reports/insight_report.md"):
    import universal_analyst_model.insight_extractor as insight_extractor
    return insight_extractor.run_insight_extraction(df, output_path)
