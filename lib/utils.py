import json
import pandas as pd
from bs4 import BeautifulSoup
import re 
from urllib.parse import urlparse

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


def clean_scraped_text(text):
    """Clean scraped text by removing html tags and unicode escape characters.
    
    Args:
        text (str): Text to clean.
        
    Returns:
        str: Cleaned text."""
    text = BeautifulSoup(text, 'html.parser').get_text().encode('utf-8').decode('unicode_escape')
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z\s\u2019\u2018\u201c\u201d\u2014]', '', text)
    return text

def get_domain(url:str) -> str:
    """Extracts the domain from a URL.

    Args:
        url (str): The URL to extract the domain from.

    Returns:
        str: The domain extracted from the URL.
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain

def convert_to_cet_timezone(x:str) -> int:
    """Convert a timestamp to Central European Time (CET).

    Args:
        x (str): The timestamp to convert.

    Returns:
        pd.Timestamp: The timestamp converted to CET.
    """
    if pd.to_datetime(x).tzinfo is None:
        return int(pd.to_datetime(x).tz_localize("CET").tz_localize(None).timestamp())
    else:
        return int(pd.to_datetime(x).tz_convert("CET").tz_localize(None).timestamp())