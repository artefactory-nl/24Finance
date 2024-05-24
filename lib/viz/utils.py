def add_emojis_to_company_description(description:str) -> str:
    """Add emojis to the company description for better readability."""
    emoji_dict = {
        'Company Overview and Business Model': '🏢📈 Company Overview and Business Model',
        'Industry and Market Conditions': '🌍📊 Industry and Market Conditions',
        'Management and Governance': '👥🗳️ Management and Governance',
        'Innovation and Research & Development': '💡🔬 Innovation and Research & Development',
        'Costs and Performance': '💰📊 Costs and Performance',
        'Top 5 Countries in which the company operates': '🌐📍 Top 5 Countries in which the company operates',
    }
    for key, value in emoji_dict.items():
        description = description.replace(key, value)
    return description