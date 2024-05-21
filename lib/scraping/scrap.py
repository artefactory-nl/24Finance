import pandas as pd
import json
from newspaper import Article
from joblib import Parallel, delayed
from lib.utils import clean_scraped_text

def extract_text_from_url(url):
    """Extracts text from a given URL using the Newspaper3k library.

    Args:
        url (str): The URL of the article to extract text from.
    
    Returns:
        str: The extracted text or an empty string if extraction fails.
    """
    try:
        article_obj = Article(url)
        article_obj.download()
        article_obj.parse()
        return article_obj.text
    except:
        return ""

def extract_text_to_dataframe(input_df: pd.DataFrame, url_column: str, output_column: str, n_jobs: int = -1):
    """Extracts the text from the URL in the input dataframe and adds it to the output column in parallel.

    Args:
        input_df (pd.DataFrame): The input dataframe.
        url_column (str): The name of the column containing the URLs.
        output_column (str): The name of the column to store the extracted text.
        n_jobs (int): The number of jobs to run in parallel (default is -1, which uses all available processors).
    
    Returns:
        pd.DataFrame: The input dataframe with the extracted text.
    """
    texts = Parallel(n_jobs=n_jobs)(
        delayed(extract_text_from_url)(url) for url in input_df[url_column]
    )
    input_df[output_column] = texts
    input_df[output_column] = input_df[output_column].apply(lambda x: json.dumps(x)).fillna("").apply(clean_scraped_text)
    return input_df.loc[(input_df[output_column] != '""')].reset_index(drop=True)
