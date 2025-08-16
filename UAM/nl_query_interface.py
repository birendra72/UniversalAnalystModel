import openai
import pandas as pd
import duckdb
import os
from typing import Optional

class NaturalLanguageQueryInterface:
    def __init__(self, df: pd.DataFrame, openai_api_key: Optional[str] = None, model_name: str = "gpt-3.5-turbo"):
        self.df = df
        self.conn = duckdb.connect(database=':memory:')
        self.conn.register('dataset', df)

        if not openai_api_key:
            raise ValueError("OpenAI API key not provided.")

        openai.api_key = openai_api_key
        self.model_name = model_name

    def query_to_sql(self, natural_language_query: str) -> str:
        # Prompt to convert natural language to SQL
        prompt = (
            "You are a helpful assistant. Convert the following natural language question "
            "into a valid SQL query using a table called 'dataset'.\n"
            f"Query: {natural_language_query}\nSQL:"
        )

        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a data analyst assistant who writes SQL queries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=150
            )

            # Handle response which might be a generator (streaming) or a normal response
            if hasattr(response, '__iter__') and not isinstance(response, (dict, list)):
                # Accumulate content from streaming chunks
                sql_query = ""
                for chunk in response:
                    # Each chunk is a dict with 'choices' key containing list of dicts with 'delta'
                    delta = chunk['choices'][0].get('delta', {})
                    content = delta.get("content", "")
                    sql_query += content
                sql_query = sql_query.strip("'\"` \n")
            elif isinstance(response, dict):
                # Non-streaming response as dict
                sql_query = response.get('choices', [{}])[0].get('message', {}).get('content', '').strip("'\"` \n")
            elif isinstance(response, list):
                if len(response) > 0:
                    sql_query = response[0]
                else:
                    sql_query = ''
            else:
                raise ValueError("Unknown response type")
    
            return sql_query

        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {e}")

    def execute_sql(self, sql_query: str) -> pd.DataFrame:
        try:
            result_df = self.conn.execute(sql_query).df()
            return result_df
        except Exception as e:
            raise RuntimeError(f"SQL execution error: {e}")

    def ask(self, natural_language_query: str) -> pd.DataFrame:
        sql_query = self.query_to_sql(natural_language_query)
        return self.execute_sql(sql_query)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Natural Language Query Interface for UAM using OpenAI')
    parser.add_argument('--datafile', type=str, required=True, help='Path to CSV data file')
    parser.add_argument('--openai_key', type=str, required=True, help='OpenAI API key')
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo', help='OpenAI model to use (e.g., gpt-3.5-turbo, gpt-4)')
    args = parser.parse_args()

    if not os.path.exists(args.datafile):
        print(f"Data file {args.datafile} does not exist.")
        exit(1)

    df = pd.read_csv(args.datafile)
    nlq = NaturalLanguageQueryInterface(df, openai_api_key=args.openai_key, model_name=args.model)

    print("🔍 Universal Analyst Model - Step 6: Natural Language Query Interface")
    print("Enter your natural language queries about the dataset. Type 'exit' to quit.")
    while True:
        query = input("Query> ")
        if query.lower() in ['exit', 'quit']:
            break
        try:
            result = nlq.ask(query)
            print(result)
        except Exception as e:
            print(f"❌ Error: {e}")
