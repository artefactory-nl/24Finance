# Description: This file contains the functions that create prompts for the different tasks in the project.
#
# The prompts are created using DeferredFString, which is a class that allows for the creation of a string template with placeholders that can be filled in later.
# The prompts are then filled in with the necessary information using the fill method of the DeferredFString class.
# The filled-in prompts are then returned as strings.
#

class DeferredFString:
    def __init__(self, template):
        self.template = template

    def fill(self, **kwargs):
        return self.template.format(**kwargs)


def create_operational_countries_prompt(fillers: dict) -> str:
    """Creates a prompt for extracting the operational countries of a company."""
    template = DeferredFString(
        """
        You are a financial expert in trading.
        I want you to list the countries in which the company {stock_name}, traded in the trade market {trading_market}, operates?
        Return the answer as a list of country codes, no other text.
        For example, if the company operates in country1 and country2, return it as ['country_code1', 'country_code2',...].
        It'simportant that you return only the list.
        """
    )
    return template.fill(**fillers)

def create_description_of_instrument_prompt(fillers: dict) -> str:
    """Creates a prompt for extracting the operational countries of a company."""
    template = DeferredFString(
        """
        I want you to provide me with a description of the company {stock_name}.
        Focus on its sector and industry in which it operates.
        Return the answer as a string, no other text.
        """
    )
    return template.fill(**fillers)

def create_news_summary_prompt(fillers: dict) -> str:
    """Creates a prompt for summarizing a news article."""
    template = DeferredFString(
        """
        I am providing you with the content of a news article. I need you to summarize it for me.
        Just return the summarised text, no other text, as a string.
        {article_content}
        """
    )
    return template.fill(**fillers)

def create_news_title_prompt(fillers: dict) -> str:
    """Creates a prompt for summarizing a news article."""
    template = DeferredFString(
        """
        I am providing you with the content of a news article. I need you to provide me with a brief title that summarizes it.
        Just return the summarised text, no other text, as a string.
        {article_content}
        """
    )
    return template.fill(**fillers)

def create_news_x_stock_impact_prompt(fillers: dict) -> str:
    """Creates a prompt for extracting the impact of a news article on a company's stocks."""
    template = DeferredFString(
        """
        You are a financial expert in trading. You read the following news article:
        "{news_content}"

        Does this news article impact your {position} position on {company_name} stocks positively or negatively? Answer with one word.
        """
    )
    return template.fill(**fillers)

def create_reason_and_impact_prompt(fillers: dict) -> str:
    """Creates a prompt for extracting reasons for the impact of a news article on a company's stocks."""
    template = DeferredFString(
        """
        You are a financial expert in trading. You read the following news article: "{news_content}"
        
        You know that this news article impacts your {company_name} stocks in a {impact} way. Give three reasons why your stocks are impacted as such. Only return the three reasons as a numbered list.
        """
    )
    return template.fill(**fillers)