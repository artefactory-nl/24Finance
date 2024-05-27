import streamlit as st
from streamlit_option_menu import option_menu
    
import os
import pandas as pd
from typing import Tuple
import plotly.express as px

st.set_page_config(
        page_title="📈 24ꜰɪɴᴀɴᴄᴇ",
)

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
def home_app():
    st.write("# 24ꜰɪɴᴀɴᴄᴇ")
    with st.container(border=True):
        st.write("""
                # Welcome
        """)
        st.write("""
                24ꜰɪɴᴀɴᴄᴇ, your ultimate companion for staying ahead of global events and understanding their impact on your investments. Our cutting-edge tool leverages the power of GenAI and advanced financial models to provide you with insightful analysis and actionable intelligence. Whether you're tracking your investment portfolio or monitoring commodities, 24ꜰɪɴᴀɴᴄᴇ ensures you stay informed and make well-founded decisions.
            """)
        st.image(os.path.join("data", "logo","logo.png"), use_column_width=True)
    with st.container(border=True):
        st.write("""
                ## Explore the Features of 24ꜰɪɴᴀɴᴄᴇ

                ### Portfolio
                In the Portfolio section, we break down the news and its financial implications for each stock in your portfolio. Here, you'll find detailed analyses of the most pertinent news articles related to your investments. Each summary comes with a financial impact assessment, and you can delve deeper by reading the full articles to understand the nuances influencing your stocks.

                ### Commodities
                The Commodities page offers a focused look at the latest news affecting various commodities. Similar to the Portfolio section, you'll see an analysis of the most significant news stories, complete with financial impact insights. This allows you to keep a pulse on the commodities market and understand the factors driving price movements.
                
                ### Summary
                Dive into the Summary page to get a comprehensive understanding of how recent news affects the sectors tied to your assets. This section provides a high-level view of the latest developments, allowing you to quickly assess the overall impact on both your investment portfolio and commodities of interest.

        """)
    with st.container(border=True):
        st.write("""
                ## How 24ꜰɪɴᴀɴᴄᴇ Works

                24ꜰɪɴᴀɴᴄᴇ uses Databricks DBRX as its large language model and gte-large for embedding, ensuring that you receive precise and relevant information. Our user-friendly interface makes it easy for you to explore summaries of relevant news, visualize their impact on your investments, and gain the insights you need to make informed decisions.

                Stay ahead of the curve with 24ꜰɪɴᴀɴᴄᴇ, where global events meet financial insight, empowering you to navigate the complexities of the market with confidence.
        """)
def overview_app():

    st.write("# 24ꜰɪɴᴀɴᴄᴇ")
    colors = ['#A3D8FF', '#FFEC9E']
    color = colors[0]
    st.markdown(f'<hr style="border-top: 3px solid {color};">', unsafe_allow_html=True)

    # Creating styled rectangle
    st.write(f"# Summary - 24ꜰɪɴᴀɴᴄᴇ Analysis")

    with st.container(border=True):
        st.write("## Stocks")
        portfolio_path = os.path.join("data",'dashboard',"portfolio_dashboard.csv")
        portfolio_df, _ = read_portfolio_data(portfolio_path)
        plot_pie_chart_by_sector(portfolio_df)

    with st.container(border=True):
        st.write("## Commodities")
        commodities_path = os.path.join("data",'dashboard',"commodities_dashboard.csv")
        commodities_df, _ = read_commodities_data(commodities_path)
        plot_pie_chart_by_sector(commodities_df)
def portfolio_app():
    st.write("# 24ꜰɪɴᴀɴᴄᴇ")
    portfolio_path = os.path.join("data",'dashboard',"portfolio_dashboard.csv")

    df, grouped = read_portfolio_data(portfolio_path)
    companies = [key for key in df.groupby('name').indices.keys()]

    with st.sidebar:
        selected_stock = option_menu(
            menu_title = "Portfolio",
            options = companies,
        )
    for i, (company_name, group_df) in enumerate(grouped):
        if company_name != selected_stock:
            continue
        else: 
            with st.container(border=True):
                st.write(f"# {group_df['name'].iloc[0]}")
                st.write(f"Sector: {group_df['sector'].iloc[0]}")
                st.write(f"Industry: {group_df['industry'].iloc[0]}")
                description_expander = st.expander("Company Description")
                with description_expander:
                    description_expander.write(f"{group_df['description'].iloc[0]}")

                st.write("---")

                for idx, row in group_df.iterrows():
                    st.write(f"### {row['Published']}   -   {row['news_title']}")
                    if row['impact'] == 'positive':
                        st.write(f"Impact: 🟩")
                    elif row['impact'] == 'negative':
                        st.write(f"Impact: 🟥")
                    else:
                        st.write(f"Impact: 🤔")
                    st.link_button("Read the article", row['Link'], type="secondary")
                    with st.expander("News Summary"):
                        st.write(row['news_summary'])
                    with st.expander("Financial Analysis"):
                        st.write(row['reasons'])
                    if idx != group_df.index[-1]:
                        st.write("---")
def commodities_app():

    st.write("# 24ꜰɪɴᴀɴᴄᴇ")
    commodities_path = os.path.join("data",'dashboard',"commodities_dashboard.csv")
    df, grouped = read_commodities_data(commodities_path)
    commodities = [key for key in df.groupby('name').indices.keys()]

    with st.sidebar:
        selected_commodity = option_menu(
            menu_title = "Commodities",
            options = commodities,
        )

    for i, (commodity, group_df) in enumerate(grouped):
        if commodity != selected_commodity:
            continue
        else: 
            with st.container(border=True):
                st.write(f"# {group_df['name'].iloc[0]}")
                st.write(f"Sector: {group_df['sector'].iloc[0]}")
                st.write(f"Industry: {group_df['industry'].iloc[0]}")

                st.write("---")

                for idx, row in group_df.iterrows():
                    st.write(f"### {row['Published']}   -   {row['news_title']}")
                    if row['impact'] == 'positive':
                        st.write(f"Impact: 🟩")
                    elif row['impact'] == 'negative':
                        st.write(f"Impact: 🟥")
                    else:
                        st.write(f"Impact: 🤔")

                    st.link_button("Read the article", row['Link'], type="secondary")
                    with st.expander("News Summary"):
                        st.write(row['news_summary'])
                    with st.expander("Financial Analysis"):
                        st.write(row['reasons'])
                    if idx != group_df.index[-1]:
                        st.write("---")
def main():
    with st.sidebar:        
        app = option_menu(
            menu_title='',
            options=['Home','Portfolio','Commodities', 'Summary'],
            default_index=0,            
            )

    if app == "Home":
        home_app()
    if app == "Summary":
        overview_app()
    if app ==  "Portfolio":
        portfolio_app()
    if app == "Commodities":
        commodities_app()
                      

if __name__ == "__main__":
    main()