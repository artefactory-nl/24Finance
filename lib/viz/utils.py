import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from typing import Tuple
import plotly.express as px


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

def plot_pie_chart_by_sector(df:pd.DataFrame):
    """Plots a pie chart for the impact of news articles by sector."""
    grouped_counts = df[df['impact'] != 'undetermined'].groupby('sector')['impact'].value_counts().unstack(fill_value=0)
    colors = {'positive': 'green', 'negative': 'red'}
    col1, col2 = st.columns(2)
    for i, (sector, counts) in enumerate(grouped_counts.iterrows()):
        counts = counts[['positive', 'negative']]  # Ensure correct order
        label_values = [count for count in counts if count > 0]
        labels = [idx for idx in counts.index if counts[idx] > 0]
        if i % 2 == 0:
            with col1:
                fig = px.pie(values=label_values, names=labels, title=sector)

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, theme=None, use_container_width=True)
                if i < len(grouped_counts) - 2:
                    st.write("---")
        else:
            with col2:
                fig = px.pie(values=label_values, names=labels, title=sector)

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, theme=None, use_container_width=True)
                if i < len(grouped_counts) - 1:
                    st.write("---")

@st.cache_data
def read_commodities_data(commodities_path:str) -> Tuple[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy]:
    """Reads the commodities data and groups it by name."""
    df = pd.read_csv(commodities_path)
    df['tmp'] = df['news_title'].apply(lambda x: len(x))
    df = (
        df.sort_values(by='tmp', ascending=False)
        .drop_duplicates(subset=['ArticleID', 'name'], keep='first').reset_index(drop=True)
        .drop(columns=['tmp'])
    )
    df['Published'] = df['Published'].apply(lambda x: pd.Timestamp(x, unit='s').strftime('%Y-%m-%d'))
    grouped = df.groupby('name')
    return df, grouped

@st.cache_data
def read_portfolio_data(portfolio_path:str) -> Tuple[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy]:
    """Reads the portfolio data and groups it by name."""
    df = pd.read_csv(portfolio_path)
    df['tmp'] = df['news_title'].apply(lambda x: len(x))
    df = (
        df.sort_values(by='tmp', ascending=False)
        .drop_duplicates(subset=['ArticleID', 'name'], keep='first').reset_index(drop=True)
        .drop(columns=['tmp'])
    )
    df['Published'] = df['Published'].apply(lambda x: pd.Timestamp(x, unit='s').strftime('%Y-%m-%d'))
    df['description'] = df['description'].apply(add_emojis_to_company_description)
    grouped = df.groupby('name')
    return df, grouped