import streamlit as st
import pandas as pd

# Assuming df is your dataframe containing the output
# you mentioned with the specified schema

# Sample DataFrame
data = {
    'Date': ['2024-04-28', '2024-04-28', '2024-04-28'],
    'EventId': [1, 2, 3],
    'stockID': ['AAPL', 'META', 'SHLL'],
    'company_name': ['Apple Inc.', 'Meta', 'Shell'],
    'industry': ['Technology', 'Technology', 'Technology'],
    'Countries': ['US', 'US', 'US'],
    'ArticleUrl': ['url1', 'url2', 'url3'],
    'NumMentions': [100, 50, 80],
    'EventName': ['Event 1', 'Event 2', 'Event 3'],
    'AvgTone': [1.2, -0.5, 0.8],
    'GoldsteinScale': [2.0, -1.0, 1.5],
    'trading_market': ['NYSE', 'NYSE', 'NASDAQ'],
    'position': ['short', 'short', 'long'],
    'news_summary': ['Summary 1', 'Summary 2', 'Summary 3'],
    'impact': ['Positive', 'Negative', 'Positive'],
    'reasons': ['Reasons 1', 'Reasons 2', 'Reasons 3']
}

df = pd.DataFrame(data)

# Grouping by stockID
grouped = df.groupby('stockID')

colors = ['#A3D8FF', '#FFEC9E']

# Displaying dashboard for each stockID
for i, (stockID, group_df) in enumerate(grouped):
    # Alternate between the two colors
    color = colors[i % len(colors)]
    st.markdown(f'<hr style="border-top: 2px solid {color};">', unsafe_allow_html=True)

    # Creating styled rectangle
    st.write(f"# {group_df['company_name'].iloc[0]}")
    st.write(f"Industry: {group_df['industry'].iloc[0]}")

    # Sorting news by NumMentions
    sorted_news = group_df.sort_values(by='NumMentions', ascending=False).head(10)

    # Displaying top 10 news
    for idx, row in sorted_news.iterrows():
        st.write(f"### {row['EventName']}")
        st.write(f"Impact: {'👍' if row['impact'] == 'Positive' else '👎'}")
        st.write(f"Countries: {group_df['Countries'].iloc[0]}")
        st.write(f"Number of Mentions: {row['NumMentions']}")
        st.write(f"[Article Url]({row['ArticleUrl']})")
        expand_key = f"{stockID}_{idx}"
        if st.checkbox("News Details & Analysis", key=expand_key):
            st.write(f"News Summary: {row['news_summary']}")
            st.write(f"Reasons: {row['reasons']}")
    st.markdown(f'<hr style="border-top: 2px solid {color};">', unsafe_allow_html=True)