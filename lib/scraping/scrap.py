import pandas as pd
import json
from newspaper import Article

def extract_text_to_dataframe(input_df:pd.DataFrame, url_column:str, output_column:str):
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
            article_obj = Article(url)
            article_obj.download()
            article_obj.parse()
            text = article_obj.text
            input_df.at[index, output_column] = text
        except:
            input_df.at[index, output_column] = ""
    input_df[output_column] = input_df[output_column].apply(lambda x: json.dumps(x)).fillna("")
    return input_df.loc[(input_df['news_content'] !='""')].reset_index(drop=True)
