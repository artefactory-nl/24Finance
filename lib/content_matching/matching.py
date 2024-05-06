import pandas as pd

def match_portfolio_and_news(news_data: pd.DataFrame, stock_df:pd.DataFrame, mentions_threshold: int = 50) -> pd.DataFrame:
    """Matches the news data with the stock data.

    Args:
        news_data (pd.DataFrame): The news data.
        stock_df (pd.DataFrame): The stock data.
        mentions_threshold (int): The threshold for the number of mentions.

    Returns:
        pd.DataFrame: The matched data.
    """
    filtered_data = pd.merge(news_data, stock_df, left_on=['ActionCountryCode'], right_on=['operational_country'], how='inner')
    filtered_data = filtered_data.loc[filtered_data['NumMentions']>= mentions_threshold]
    filtered_data = filtered_data[
        ['Date', 'EventId', 'stockID', 'company_name', 'company_description', 'industry', 'operational_country', 'ArticleUrl', 'NumMentions', 'AvgTone', 'GoldsteinScale', 'trading_market', 'position']
        ].reset_index(drop=True)
    return filtered_data