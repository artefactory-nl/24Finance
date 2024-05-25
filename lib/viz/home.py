    
import streamlit as st
import pandas as pd
import tomli
import sys
import os

def app():

    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.append(cwd)

    with open(os.path.join(cwd, "config", "config.toml"), "rb") as f:
        config = tomli.load(f)
    
    with st.container(border=True):
        st.write("""
                # Welcome to 24ꜰɪɴᴀɴᴄᴇ
        """)
        st.write("""
                24ꜰɪɴᴀɴᴄᴇ, your ultimate companion for staying ahead of global events and understanding their impact on your investments. Our cutting-edge tool leverages the power of GenAI and advanced financial models to provide you with insightful analysis and actionable intelligence. Whether you're tracking your investment portfolio or monitoring commodities, 24ꜰɪɴᴀɴᴄᴇ ensures you stay informed and make well-founded decisions.
            """)
        st.image(os.path.join(cwd, "data", "logo","logo.png"), use_column_width=True)
    with st.container(border=True):
        st.write("""
                ## Explore the Features of 24ꜰɪɴᴀɴᴄᴇ

                ### Overview
                Dive into the Overview page to get a comprehensive understanding of how recent news affects the sectors tied to your assets. This section provides a high-level view of the latest developments, allowing you to quickly assess the overall impact on both your investment portfolio and commodities of interest.

                ### Portfolio
                In the Portfolio section, we break down the news and its financial implications for each stock in your portfolio. Here, you'll find detailed analyses of the most pertinent news articles related to your investments. Each summary comes with a financial impact assessment, and you can delve deeper by reading the full articles to understand the nuances influencing your stocks.

                ### Commodities
                The Commodities page offers a focused look at the latest news affecting various commodities. Similar to the Portfolio section, you'll see an analysis of the most significant news stories, complete with financial impact insights. This allows you to keep a pulse on the commodities market and understand the factors driving price movements.
        """)
    with st.container(border=True):
        st.write("""
                ## How 24ꜰɪɴᴀɴᴄᴇ Works

                24ꜰɪɴᴀɴᴄᴇ uses Databricks DBRX as its large language model and gte-large for embedding, ensuring that you receive precise and relevant information. Our user-friendly interface makes it easy for you to explore summaries of relevant news, visualize their impact on your investments, and gain the insights you need to make informed decisions.

                Stay ahead of the curve with 24ꜰɪɴᴀɴᴄᴇ, where global events meet financial insight, empowering you to navigate the complexities of the market with confidence.
        """)