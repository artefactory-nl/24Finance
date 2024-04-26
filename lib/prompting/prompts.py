class DeferredFString:
    def __init__(self, template):
        self.template = template

    def fill(self, **kwargs):
        return self.template.format(**kwargs)


def create_operational_countries_prompt(fillers: dict) -> str:
    template = DeferredFString(
        """
        What are the countries in which {stock_id}, {description}, operates?
        Return the answer as a python list of countries names only, no other text,
        such as ['el1', 'el2',...].
        """
    )
    return template.fill(**fillers)


def create_news_summary_prompt(fillers: dict) -> str:
    template = DeferredFString(
        """

        """
    )
    return template.fill(**fillers)


def create_impact_prompt(fillers: dict) -> str:
    template = DeferredFString(
        """
        """
    )
    return template.fill(**fillers)
