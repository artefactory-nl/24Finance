import json
import pandas as pd
from newspaper import Article

def extract_text_to_dataframe(input_df:pd.DataFrame, url_column:str, output_column:str) -> pd.DataFrame:
    """Extracts the text from the URL in the input dataframe and adds it to the output column.

    Args:
        input_df (pd.DataFrame): The input dataframe.
        url_column (str): The name of the column containing the URLs.
        output_column (str): The name of the column to store the extracted text.

    Returns:
        pd.DataFrame: The input dataframe with the extracted text.
    """
    for index, row in input_df.iterrows():
        url = row[url_column]
        try:
            article = Article(url)
            article.download()
            article.parse()
            text = article.text
            input_df.at[index, output_column] = text
        except Exception as e:
            print(f"Error processing URL {url}: {str(e)}")
    input_df[output_column] = input_df[output_column].apply(lambda x: json.dumps(x))
    return input_df

def extract_list_from_text(text:str):
    """Extracts a list from a string."""
    start_index = text.find("[")
    end_index = text.find("]")+1
    return eval(text[start_index:end_index])