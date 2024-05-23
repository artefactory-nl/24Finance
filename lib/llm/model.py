from openai import OpenAI
import yaml
from pathlib import Path
from lib.prompting.prompts import (
    create_operational_countries_prompt,
    create_news_x_stock_impact_prompt,
    create_reason_and_impact_prompt,
    create_news_summary_prompt,
    create_news_title_prompt,
    create_description_of_instrument_prompt,
)
from lib.utils import extract_list_from_text

def model_api_client() -> object:
    """Returns an instance of the OpenAI API client."""
    secrets_file = Path(__file__).resolve().parent.parent.parent / 'secrets' / 'secrets.yaml'
    with open(secrets_file) as f:
        secrets = yaml.safe_load(f)
    return OpenAI(
        api_key=secrets['dbrx']['api_token'],
        base_url=secrets['dbrx']['api_url'],
    )


def prompt_llm(client: object, prompt: str = "", role: str = "", temperature: int = 0.3) -> str:
    """Interacts with the LLM model to generate a response given the
    prompt and fillers.

    This function uses the OpenAI API client to interact with the LLM model.
    It sends a chat completion request to the model with a system message and a user message.
    The system message contains the role of the user and the user message is generated by filling the prompt with the provided fillers.
    The model then generates a response based on these messages.

    Args:
        client (object): An instance of the OpenAI API client.
        prompt (str): The prompt to be used for generating the response. This is a string that contains placeholders for the fillers.
        role (str): The role of the user. This is used in the system message sent to the model.
        temperature (int): The temperature parameter for the model. This controls the randomness of the generated response.

    Returns:
        str: The generated response from the LLM model.
    """
    return client.chat.completions.create(
        messages=[
            {"role": "system", "content": f"{role}"},
            {"role": "user", "content": f"{prompt}"},
        ],
        model="dbrx",   #"mixtral-chat",
        temperature=temperature,
    )

def make_operational_countries(row:object, client:object) -> list:
    """Extracts the operational countries of a company from the LLM model.
    
    Args:
        row (dict): A dataframe row containing the company name and trading market.
        client (object): An instance of the OpenAI API client.
        
    Returns:
        list: A list of operational countries.
    """
    role = "Financial expert in trading."
    fillers = {
        'stock_name': row['company_name'],
        'trading_market': row['trading_market'],
        }
    prompt = create_operational_countries_prompt(fillers)
    max_attempts = 5
    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        countries = prompt_llm(client, prompt=prompt, role=role).choices[0].message.content
        try:
            countries_list = extract_list_from_text(countries)
            return countries_list
        except:
            pass
    return []

def make_description_of_instrument(row:object, client:object) -> str:
    """Extracts the description of a company from the LLM model.
    
    Args:
        row (dict): A dataframe row containing the company name.
        client (object): An instance of the OpenAI API client.
        
    Returns:
        str: A description of the company.
    """
    role = "Financial expert in trading."
    fillers = {
        'name': row['name'],
        'ticker': row['ticker'],
        'sector': row['sector'],
        'industry': row['industry'],
        'headquarters': row['headquarters'],
        }
    prompt = create_description_of_instrument_prompt(fillers)
    description = prompt_llm(client, prompt=prompt, role=role).choices[0].message.content
    return description

def make_summary_from_news(row: object, client: object) -> str:
    """Summarize the news article.

    Args:
        row (object): A dataframe row containing the news content.
        client (object): An instance of the OpenAI API client.

    Returns:
        str: The summary of the news article.
    """
    role = "Financial expert in trading with expertise as a journalist."
    fillers={
        'article_content': row['news_content'],
    }
    prompt = create_news_summary_prompt(fillers)
    summary = prompt_llm(client, prompt=prompt, role=role).choices[0].message.content
    return summary

def make_title_from_news(row: object, client: object) -> str:
    """Summarize the news article to produce a title.

    Args:
        row (object): A dataframe row containing the news content.
        client (object): An instance of the OpenAI API client.

    Returns:
        str: The summary of the news article.
    """
    role = "Financial expert in trading with expertise as a journalist."
    fillers={
        'article_content': row['news_content'],
    }
    prompt = create_news_title_prompt(fillers)
    summary = prompt_llm(client, prompt=prompt, role=role).choices[0].message.content
    return summary

def make_impact_from_news(row: object, client: object) -> str:
    """ Return either "positive" or "negative" for impact.
    
    Args:
        row (object): A dataframe row containing the news content, position, and company name.
        client (object): An instance of the OpenAI API client.

    Returns:
        str: The impact of the news article on the company's stocks. This can be "positive" or "negative".
    """
    role = "Financial expert in trading."
    fillers={
        'news_content': row['news_content'],
        'position': row['position'],
        'company_name': row['company_name']
    }

    prompt = create_news_x_stock_impact_prompt(fillers)
    trials = 0
    correct = False
    impact = "undetermined"
    while (trials < 4) and not correct:
        result = prompt_llm(client, prompt=prompt, role=role).choices[0].message.content
        if result.lower()[0:8] == "positive":
            correct = True
            impact = "positive"
        elif result.lower()[0:8] == "negative":
            correct = True
            impact = "negative"
        trials = trials + 1
    return impact

def make_reasons_from_news(row: object, client: object) -> str:    
    """ Return three reasons for the impact.

    The reasons should be returned as a numbered list.

    Args:
        row (object): A dataframe row containing the news content, impact, and company name.
        client (object): An instance of the OpenAI API client.

    Returns:
        str: The three reasons for the impact of the news article on the company's stocks.    
    """
    role = "Financial expert in trading."
    fillers={
        'news_content': row['news_content'],
        'impact': row['impact'],
        'company_name': row['company_name']
    }

    prompt = create_reason_and_impact_prompt(fillers)
    reasons = prompt_llm(client, prompt=prompt, role=role).choices[0].message.content
    return reasons