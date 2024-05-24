import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import tomli
import sys
import os

cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.append(cwd)

from lib.viz.utils import add_emojis_to_company_description

with open(os.path.join(cwd, "config", "config.toml"), "rb") as f:
    config = tomli.load(f)

comodities = ['Gold', 'Silver', 'Oil', 'Copper', 'Platinum', 'Palladium']

df = pd.read_csv(os.path.join(cwd, config["data"]["location"], config["data"]['dashboard']["location"],config["data"]['dashboard']["filename"]))
df['tmp'] = df['news_title'].apply(lambda x: len(x))
df = (
    df.sort_values(by='tmp', ascending=False)
    .drop_duplicates(subset=['Link'], keep='first').reset_index(drop=True)
    .drop(columns=['tmp'])
)
df['Published'] = df['Published'].apply(lambda x: pd.Timestamp(x, unit='s').strftime('%Y-%m-%d'))
df['description'] = df['description'].apply(add_emojis_to_company_description)
grouped = df.groupby('name')
companies = [key for key in df.groupby('name').indices.keys()]
colors = ['#A3D8FF', '#FFEC9E']
st.write("# 24ꜰɪɴᴀɴᴄᴇ")

def on_change_stock(key):
    st.session_state.count = 0
    # st.write(f"{st.session_state.count}")

def on_change_comodity(key):
    st.session_state.count = 1
    # st.write(f"{st.session_state.count}")

st.session_state.count = 0
with st.sidebar:
    with st.sidebar:
        selected_stock = option_menu(
            menu_title = "Portfolio",
            options = companies,
            on_change=on_change_stock,
            key="stock_menu"
    )
        selected_comodity = option_menu(
            menu_title = "Comodities",
            options = comodities,
            on_change=on_change_comodity,
            key="comodity_menu"
        )

# if st.session_state.count == 0:
#     st.write(f"Selected Stock: {selected_stock}")

# elif st.session_state.count == 1:
#     st.write(f"Selected Comodity: {selected_comodity}")

for i, (company_name, group_df) in enumerate(grouped):
    if company_name != selected_stock:
        continue
    else: 
        with st.container(border=True):
            # Alternate between the two colors
            color = colors[i % len(colors)]
            st.markdown(f'<hr style="border-top: 3px solid {color};">', unsafe_allow_html=True)

            # Creating styled rectangle
            st.write(f"# {group_df['name'].iloc[0]}")
            st.write(f"Sector: {group_df['industry'].iloc[0]}")
            st.write(f"Industry: {group_df['industry'].iloc[0]}")
            st.write(f"Description: \n\n{group_df['description'].iloc[0]}")

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
                with st.popover("News Summary"):
                    st.write(row['news_summary'])
                with st.popover("Financial Analysis"):
                    st.write(row['reasons'])
                st.write("---")
            st.markdown(f'<hr style="border-top: 2px solid {color};">', unsafe_allow_html=True)

# for i, comodity in enumerate(comodities):
#     if selected_stock is not None:
#         break
#     if comodity != selected_comodity:
#         continue
#     else: 
#         selected_stock = None
#         with st.container(border=True):
#             # Alternate between the two colors
#             color = colors[i % len(colors)]
#             st.markdown(f'<hr style="border-top: 3px solid {color};">', unsafe_allow_html=True)

#             # Creating styled rectangle
#             st.write(f"# {comodity}")
#             st.write(f"# {comodity}")
#             st.write(f"# {comodity}")

#             st.write("---")
#             st.markdown(f'<hr style="border-top: 2px solid {color};">', unsafe_allow_html=True)