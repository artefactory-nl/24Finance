import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
        page_title="📈 24ꜰɪɴᴀɴᴄᴇ",
)

from lib.viz import home, overview, portfolio, commodities

def main():
    with st.sidebar:        
        app = option_menu(
            menu_title='',
            options=['Home','Overview','Portfolio','Commodities'],
            default_index=0,            
            )

    if app == "Home":
        home.app()
    if app == "Overview":
        overview.app()
    if app ==  "Portfolio":
        portfolio.app()
    if app == "Commodities":
        commodities.app()
                      

if __name__ == "__main__":
    main()