from lib.llm.model import prompt_llm
import ast
class DeferredFString:
    def __init__(self, template):
        self.template = template

    def fill(self, **kwargs):
        return self.template.format(**kwargs)


def create_operational_countries_prompt(fillers: dict) -> str:
    template = DeferredFString(
        """
        What are the countries in which the company {stock_name}, traded in the trade market {trading_market} operates?
        Return the answer as a python list of countries, names only, no other text,
        such as ['country1', 'country2',...].
        Use CAMEO codes to identify the countries.
        """
    )
    return template.fill(**fillers)


def create_news_summary_prompt(fillers: dict) -> str:
    template = DeferredFString(
        """
        I am providing you with the content of a news article. I need you to summarize it for me.
        Just return the summarised text, no other text, as a string.
        {article_content}
        """
    )
    return template.fill(**fillers)


def create_impact_prompt(fillers: dict) -> str:
    template = DeferredFString(
        """
        """
    )
    return template.fill(**fillers)


def extract_operational_countries(client, row, role) -> list:
    """Extracts the operational countries of a company from the LLM model."""
    fillers = {
        'stock_name': row['company_name'],
        'trading_market': row['trading_market'],
        }
    prompt = create_operational_countries_prompt(fillers)
    countries = prompt_llm(client, prompt=prompt, role=role).choices[0].message.content
    countries_list = ast.literal_eval(countries)
    return countries_list
