    
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import tomli
import sys
import os

def app():

    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.append(cwd)

    from lib.viz.utils import read_portfolio_data

    with open(os.path.join(cwd, "config", "config.toml"), "rb") as f:
        config = tomli.load(f)

    st.write("# 24ꜰɪɴᴀɴᴄᴇ")
    portfolio_path = os.path.join(cwd, config["data"]["location"], config["data"]['dashboard']["location"],config["data"]['dashboard']["filename_portfolio"])

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
                # Alternate between the two colors
                # Creating styled rectangle
                st.write(f"# {group_df['name'].iloc[0]}")
                st.write(f"Sector: {group_df['sector'].iloc[0]}")
                st.write(f"Industry: {group_df['industry'].iloc[0]}")
                description_expander = st.expander("Company Description")
                with description_expander:
                    description_expander.write(f"{group_df['description'].iloc[0]}")

                st.write("---")

                # Displaying top 10 news
                for idx, row in group_df.iterrows():
                    st.write(f"### {row['Published']}   -   {row['news_title']}")
                    impact, sentiment = st.columns(2)
                    with impact:
                        if row['impact'] == 'positive':
                            st.write(f"Impact: 🟩")
                        elif row['impact'] == 'negative':
                            st.write(f"Impact: 🟥")
                        else:
                            st.write(f"Impact: 🤔")

                    with sentiment:
                        if row['impact'] == 'positive':
                            st.write(f"Impact: 🟩")
                        elif row['impact'] == 'negative':
                            st.write(f"Impact: 🟥")
                        else:
                            st.write(f"Impact: 🤔")
                    # st.write(f"Countries: {group_df['operational_country'].iloc[0]}")
                    st.link_button("Read the article", row['Link'], type="secondary")
                    with st.expander("News Summary"):
                        st.write(row['news_summary'])
                    with st.expander("Financial Analysis"):
                        st.write(row['reasons'])
                    if idx != group_df.index[-1]:
                        st.write("---")
