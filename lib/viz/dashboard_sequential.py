import streamlit as st
import pandas as pd
from pathlib import Path

df = pd.read_csv(Path(__file__).parent.parent.parent / 'data' / 'news_data_processed.csv')

# Grouping by stockID
grouped = df.groupby('stockID')

colors = ['#A3D8FF', '#FFEC9E']
st.write("# 24ꜰɪɴᴀɴᴄᴇ")
# Displaying dashboard for each stockID
for i, (stockID, group_df) in enumerate(grouped):
    sorted_news = (
        group_df.dropna()
        .loc[
            (group_df['news_content'] !='""')
            & ((group_df['impact'] =='positive') | (group_df['impact'] =='negative'))

            ]
        .sort_values(by=['Date','NumMentions'], ascending=[False,False]).head(5)        
    )
    if sorted_news.empty:
        continue
    else:
        with st.container(border=True):
            # Alternate between the two colors
            color = colors[i % len(colors)]
            st.markdown(f'<hr style="border-top: 3px solid {color};">', unsafe_allow_html=True)

            # Creating styled rectangle
            st.write(f"# {group_df['company_name'].iloc[0]}")
            st.write(f"Industry: {group_df['industry'].iloc[0]}")

            # Displaying top 10 news
            for idx, row in sorted_news.iterrows():
                st.write(f"### {row['Date'].replace('-','.')}   -   {row['EventName']}")
                impact, sentiment = st.columns(2)
                with impact:
                    if row['impact'] == 'positive':
                        st.write(f"Impact: 👍")
                    elif row['impact'] == 'negative':
                        st.write(f"Impact: 👎")
                    else:
                        st.write(f"Impact: 🤔")

                with sentiment:
                    if row['GoldsteinScale'] >= 0 and row['AvgTone'] >= 0:
                        st.write(f"International relations: 😁")
                    elif row['GoldsteinScale'] <= 0 and row['AvgTone'] <= 0:
                        st.write(f"International relations: 😟")
                    else:
                        st.write(f"International relations: 😐")
                st.write(f"Countries: {group_df['Countries'].iloc[0]}")
                st.write(f"Number of Mentions: {row['NumMentions']}")
                st.link_button("Read the article", row['ArticleUrl'], type="secondary")
                with st.popover("News Summary"):
                    st.write(row['news_summary'])
                with st.popover("Financial Analysis"):
                    st.write(row['reasons'])
                st.write("---")
            st.markdown(f'<hr style="border-top: 2px solid {color};">', unsafe_allow_html=True)