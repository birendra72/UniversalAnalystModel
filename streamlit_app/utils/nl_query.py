import openai
import duckdb
import pandas as pd

class NaturalLanguageQueryInterface:
    def __init__(self, df: pd.DataFrame, openai_api_key: str, model_name: str = "gpt-3.5-turbo"):
        if not openai_api_key:
            raise ValueError("OpenAI API key must be provided and non-empty")
        self.df = df
        self.conn = duckdb.connect(database=':memory:')
        self.conn.register('dataset', df)
        openai.api_key = openai_api_key
        self.model_name = model_name

    def query_to_sql(self, natural_language_query: str) -> str:
        prompt = (
            "You are a helpful assistant. Convert the following natural language question "
            "into a valid SQL query using a table called 'dataset'.\n"
            f"Query: {natural_language_query}\nSQL:"
        )
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a data analyst assistant who writes SQL queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=150
        )
        # Defensive check for response type
        if isinstance(response, dict) and 'choices' in response:
            sql_query = response['choices'][0]['message']['content'].strip()
        else:
            sql_query = ""
        return sql_query

    def execute_sql(self, sql_query: str) -> pd.DataFrame:
        return self.conn.execute(sql_query).df()

    def ask(self, natural_language_query: str) -> pd.DataFrame:
        sql_query = self.query_to_sql(natural_language_query)
        return self.execute_sql(sql_query)

def process_query(df: pd.DataFrame, query: str, api_key: str = None):
    if api_key is None or api_key == "":
        raise ValueError("OpenAI API key must be provided and non-empty")
    nlq = NaturalLanguageQueryInterface(df, openai_api_key=api_key)
    return nlq.ask(query)
