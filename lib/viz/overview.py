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

    from lib.viz.utils import read_commodities_data, plot_pie_chart_by_sector

    with open(os.path.join(cwd, "config", "config.toml"), "rb") as f:
        config = tomli.load(f)

    from lib.viz.utils import read_portfolio_data, read_commodities_data

    st.write("# 24ꜰɪɴᴀɴᴄᴇ")
    colors = ['#A3D8FF', '#FFEC9E']
    color = colors[0]
    st.markdown(f'<hr style="border-top: 3px solid {color};">', unsafe_allow_html=True)

    # Creating styled rectangle
    st.write(f"# Overview - 24ꜰɪɴᴀɴᴄᴇ Analysis")

    with st.container(border=True):
        st.write("## Stocks")
        portfolio_path = os.path.join(cwd, config["data"]["location"], config["data"]['dashboard']["location"],config["data"]['dashboard']["filename_portfolio"])
        portfolio_df, _ = read_portfolio_data(portfolio_path)
        plot_pie_chart_by_sector(portfolio_df)

    with st.container(border=True):
        st.write("## Commodities")
        commodities_path = os.path.join(cwd, config["data"]["location"], config["data"]['dashboard']["location"],config["data"]['dashboard']["filename_commodities"])
        commodities_df, _ = read_commodities_data(commodities_path)
        plot_pie_chart_by_sector(commodities_df)
