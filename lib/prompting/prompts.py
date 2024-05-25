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


def create_description_of_instrument_prompt(fillers: dict) -> str:
    """Creates a prompt for extracting the operational countries of a company."""
    template = DeferredFString(
        """
            You are a financial expert in trading.

            These are the details of the company I need you to focus on:
            - name: {name},
            - stock ticker: {ticker},
            - sector: {sector},
            - industry: {industry},
            - headquarters location: {headquarters},

            Provide me with a description of this company, following this structure:
            - Company Overview and Business Model
            - Industry and Market Conditions
            - Management and Governance: 
            - Innovation and Research & Development (R&D)
            - what does it depend on in terms of costs and performance
            - top 5 countries in which the company operates and why

            Provide me with just the answer, no introduction or final summary.
        """
    )
    return template.fill(**fillers)

def create_news_summary_prompt(fillers: dict) -> str:
    """Creates a prompt for summarizing a news article."""
    template = DeferredFString(
        """
        You are a financial expert in trading with expertise as a journalist.
        I am providing you with a news article:
        - title: "{article_title}",
        - content: "{article_content}"
        
        I need you to provide me with a brief summary of the news article.
        Just return the summarised text, no other text, as a string.
        """
    )
    return template.fill(**fillers)

def create_news_title_prompt(fillers: dict) -> str:
    """Creates a prompt for summarizing a news article."""
    template = DeferredFString(
        """
        You are a financial expert in trading with expertise as a journalist.
        I am providing you with a news article:
        - title: "{article_title}",
        - content: "{article_content}"

        I need you to provide me with a brief title that summarizes it.
        Just return the summarised text, no other text, as a string.
        """
    )
    return template.fill(**fillers)

def create_news_x_stock_impact_prompt(fillers: dict) -> str:
    """Creates a prompt for extracting the impact of a news article on a company's stocks."""
    template = DeferredFString(
        """
        You are a financial expert in trading.

        The context is made of a news article you read and of the details of a company of which you own stocks.
        - You read the following news article: "{news_content}"

        - You own stocks of the company {company_name} and these are its details:
            - name: {company_name},
            - stock ticker: {company_ticker},
            - sector: {company_sector},
            - industry: {company_industry},
            - description: {company_description}

        Does this news article impact the {company_name}'s stocks positively or negatively?
        Answer with one word: either "positive" or "negative".
        """
    )
    return template.fill(**fillers)

def create_reasons_of_impact_on_stock_prompt(fillers: dict) -> str:
    """Creates a prompt for extracting reasons for the impact of a news article on a company's stocks."""
    template = DeferredFString(
        """
        You are a financial expert in trading.

        The context is made of a news article you read and of the details of a company of which you own stocks.
        - You read the following news article:
        "{news_content}"

        - You own stocks of the company {company_name} and these are its details:
            - name: {company_name},
            - stock ticker: {company_ticker},
            - sector: {company_sector},
            - industry: {company_industry},
            - description: {company_description}

        You know that this news article impacts your {company_name} stocks in a {impact} way.
        Give a maximum of three reasons why your stocks are impacted as such.
        Only return the three reasons as a numbered list.
        """
    )
    return template.fill(**fillers)

def create_news_x_commodity_impact_prompt(fillers: dict) -> str:
    """Creates a prompt for extracting the impact of a news article on a company's stocks."""
    template = DeferredFString(
        """
        You are a financial expert in trading.
        I want to understand the impact of the news on the commodities.

        The context is made of a news article you read and of the details of a commodity.
        - You read the following news article:
        "{news_content}"

        - You depend on the following commodity and these are its details:
            - name: {name},
            - sector: {sector},
            - industry: {industry},

        Does this news article impact the commodity "{name}" positively or negatively?
        Answer with one word: either "positive" or "negative".
        """
    )
    return template.fill(**fillers)

def create_reasons_of_impact_on_commodity_prompt(fillers: dict) -> str:
    """Creates a prompt for extracting reasons for the impact of a news article on a company's stocks."""
    template = DeferredFString(
        """
        You are a financial expert in trading.
        I want to understand why certain news had an impact on the commodities.

        The context is made of a news article you read and of the details of a company of which you own stocks.
        - You read the following news article:
        "{content}"

        - You depend on the following commodity and these are its details:
            - name: {name},
            - sector: {sector},
            - industry: {industry},

        You know that this news article impacts the commodity "{name}" in a {impact} way.
        Give a maximum of three reasons why your stocks are impacted as such.
        Only return the three reasons as a numbered list.
        """
    )
    return template.fill(**fillers)