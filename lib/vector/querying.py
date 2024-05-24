from lib.prompting.prompts import DeferredFString
from typing import List, Dict

def create_news_info_retrieval_query(fillers: dict) -> str:
    """Creates a prompt for summarizing a news article."""
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

def make_news_retrieval(row: object, chroma_client:object, filters: Dict = {}, top_k_results:int=10) -> List:
    """Retrieves news articles relevant to a company from a news vector database.

    Args:
        row (object): A dataframe row containing the company information.
        chroma_client (object): An instance of the Chroma client.
        filters (dict): Filters to apply to the search query.
        top_k_results (int): The number of results to return.

    Returns:
        List: A list of news articles relevant to the company.
    """
    match_list = []  
    fillers={
        'name': row['name'],
        'ticker': row['ticker'],
        'sector': row['sector'],
        'industry': row['industry'],
        'description': row['description'],
    }
    query = create_news_info_retrieval_query(fillers)

    results = chroma_client.as_retriever(
          search_kwargs={
            "k": top_k_results,
            "filter": filters,
            }
    ).get_relevant_documents(query)
    for result in results:                
            match = result.metadata
            match['ticker'] = row['ticker']
            match['Content'] = result.page_content
            match_list.append(match)
    return match_list