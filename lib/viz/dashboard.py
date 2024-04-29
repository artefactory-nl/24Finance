import streamlit as st
import pandas as pd
from pathlib import Path

df = pd.read_csv(Path(__file__).parent.parent.parent / 'data' / 'news_data_processed.csv')

# Grouping by stockID
grouped = df.groupby('stockID')

colors = ['#A3D8FF', '#FFEC9E']

# Displaying dashboard for each stockID
for i, (stockID, group_df) in enumerate(grouped):
    sorted_news = group_df.loc[group_df['impact']!='undetermined'].sort_values(by='NumMentions', ascending=False).head(10)
    if sorted_news.empty:
        continue
    # Alternate between the two colors
    color = colors[i % len(colors)]
    st.markdown(f'<hr style="border-top: 2px solid {color};">', unsafe_allow_html=True)

    # Creating styled rectangle
    st.write(f"# {group_df['company_name'].iloc[0]}")
    st.write(f"Industry: {group_df['industry'].iloc[0]}")

    # Displaying top 10 news
    for idx, row in sorted_news.iterrows():
        st.write(f"### {row['EventName']}")
        if row['impact'] == 'positive':
            st.write(f"Impact: 👍")
        elif row['impact'] == 'negative':
            st.write(f"Impact: 👎")
        else:
            st.write(f"Impact: 🤔")
        st.write(f"Countries: {group_df['Countries'].iloc[0]}")
        st.write(f"Number of Mentions: {row['NumMentions']}")
        st.write(f"[Article Url]({row['ArticleUrl']})")
        expand_key = f"{stockID}_{idx}"
        if st.checkbox("News Details & Analysis", key=expand_key):
            st.write(f"News Summary:\n\n{row['news_summary']}")
            st.write(f"Reasons: \n{row['reasons']}")
    st.markdown(f'<hr style="border-top: 2px solid {color};">', unsafe_allow_html=True)