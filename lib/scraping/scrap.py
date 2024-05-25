import pandas as pd
import json
import yaml
from typing import List
import feedparser
from newspaper import Article
from joblib import Parallel, delayed
from lib.utils import clean_scraped_text, get_domain

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

def extract_news_content_from_url_to_dataframe(input_df: pd.DataFrame, url_column: str, output_column: str, n_jobs: int = -1):
    """Extracts the text from the URL in the input dataframe and adds it to the output column in parallel.

    Args:
        input_df (pd.DataFrame): The input dataframe.
        url_column (str): The name of the column containing the URLs.
        output_column (str): The name of the column to store the extracted text.
        n_jobs (int): The number of jobs to run in parallel (default is -1, which uses all available processors).
    
    Returns:
        pd.DataFrame: The input dataframe with the extracted text.
    """
    urls = input_df[url_column].tolist()
    texts = Parallel(n_jobs=n_jobs)(
        delayed(extract_text_from_url)(url) for url in urls
    )
    input_df
    input_df[output_column] = texts
    input_df[output_column] = input_df[output_column].apply(lambda x: json.dumps(x)).fillna("").apply(clean_scraped_text)
    return input_df.loc[(input_df[output_column] != '""')].reset_index(drop=True)

def parse_rss_feed(url: str) -> List:
    """Parses an RSS feed and returns a list of dictionaries containing the feed entries.

    Args:
        url (str): The URL of the RSS feed to parse.

    Returns:
        List: A list of dictionaries containing the feed entries.
    """
    try:
        feed = feedparser.parse(url)
        domain = get_domain(url)
        print(f"Processed {domain}.")
        return [{
            "Title": entry.get("title",""),
            "Link": entry.get("link",""),
            "Published": entry.get("published",""),
            "Summary": entry.get("summary",""),
            "Source": domain,
        } for entry in feed.entries]
    except:
        return []


def collect_rss_feed(rss_urls: List[str]) -> pd.DataFrame:
    """Collects RSS feeds in parallel and returns a DataFrame of the feed entries.

    Args:
        rss_urls (List[str]): A list of URLs of the RSS feeds to collect.

    Returns:
        pd.DataFrame: A DataFrame containing the feed entries.
    """
    all_news_items = Parallel(n_jobs=-1)(delayed(parse_rss_feed)(url) for url in rss_urls)

    return pd.DataFrame([item for sublist in all_news_items for item in sublist])

def load_rss_urls_from_config(config_file_path: str) -> List[str]:
    """Loads RSS URLs from a configuration file.

    Args:
        config_file_path (str): The path to the configuration file.

    Returns:
        List[str]: A list of RSS URLs.
    """
    with open(config_file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config['rss_urls']