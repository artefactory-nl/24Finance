from lib.prompting.prompts import DeferredFString
from typing import List, Dict

def retrieve_from_news(row:object, chroma_client:object, reference_col:str, mode:str, filters: Dict = {}, top_k_results:int=10) -> List:
    """Retrieves news articles relevant to a stock or a commodity from a news vector database.

    Args:
        row (object): A dataframe row containing the company information.
        chroma_client (object): An instance of the Chroma client.
        reference_col (str): The name of the column containing the reference.
        mode (str): The mode of the query ('stocks' or 'commodities').
        filters (dict): Filters to apply to the search query.
        top_k_results (int): The number of results to return.

    Returns:
        List: A list of news articles relevant to the stock or commodity.
    """

    if mode == 'stocks':
        query = make_stock_news_query(row)
    elif mode == 'commodities':
        query = make_commodities_news_query(row)

    match_list = []
    results = chroma_client.as_retriever(
          search_kwargs={
            "k": 100,
            "filter": filters,
            }
    ).get_relevant_documents(query)
    for result in results:                
            match = result.metadata
            match[reference_col] = row[reference_col]
            match['Content'] = result.page_content
            match_list = add_unique_dict(match_list, match, ['ArticleID'])
    if top_k_results > len(match_list):
        return match_list
    return match_list[:top_k_results]

def make_stock_news_query(row: object) -> List:
    """Creates a query to retrieve news articles relevant to a company.
    
    Args:
        row (object): A dataframe row containing the company information.
        
    Returns:
        List: A list of news articles relevant to the company.
    """
    fillers={
        'name': row['name'],
        'ticker': row['ticker'],
        'sector': row['sector'],
        'industry': row['industry'],
        'description': row['description'],
    }
    return create_stock_news_query(fillers)

def create_stock_news_query(fillers: dict) -> str:
    """Creates a query to retrieve news articles relevant to a company."""
    template = DeferredFString("""
                Given as context:
                - name of the company: {name}
                - ticker of the company: {ticker}
                - sector of the company: {sector}
                - industry of the company: {industry}
                - description of the company: {description}

                Find the most relevant news articles for the company, focusing on the ones that might have an impact on the company's stock price.
        """
    )
    return template.fill(**fillers)


def make_commodities_news_query(row: object) -> List:
    """Creates a query to retrieve news articles relevant to a commodity.

    Args:
        row (object): A dataframe row containing the commodity information.

    Returns:
        List: A list of news articles relevant to the commodity.
    """
    fillers={
        'name': row['name'],
        'sector': row['sector'],
        'industry': row['industry'],
    }
    return create_commodities_news_query(fillers)


def create_commodities_news_query(fillers: dict) -> str:
    """Creates a query to retrieve news articles relevant to a commodity."""
    template = DeferredFString("""
                I want to understand the impact of the news on the commodities.
                Here the context of the commodity I am interested in:
                - name of the commodity: {name}
                - sector of the commodity: {sector}
                - industry of the commodity: {industry}

                Find the most relevant news articles for the commodity, focusing on the ones that might have an impact on the commodity's price.
        """
    )
    return template.fill(**fillers)

def add_unique_dict(dict_list: List[Dict], new_dict: Dict, unique_fields:List[str]) -> List[Dict]:
    """Adds a new dictionary to a list of dictionaries if it does not contain duplicate fields.

    Args:
        dict_list (List[Dict]): The list of dictionaries.
        new_dict (Dict): The new dictionary to add.
        unique_fields (List[str]): The fields that should be unique in the dictionary.

    Returns:
        List[Dict]: The updated list of dictionaries.
    """
    for existing_dict in dict_list:
        if all(existing_dict.get(field) == new_dict.get(field) for field in unique_fields):
            return dict_list

    dict_list.append(new_dict)
    return dict_list