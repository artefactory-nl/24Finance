# Databricks notebook source
import newspaper
import pandas as pd
import json

# COMMAND ----------

df = spark.sql("select * from hive_metastore.default.stock_data WHERE stockID is not NULL")

# COMMAND ----------

# MAGIC %md
# MAGIC <b>UTILS</b>
# MAGIC
# MAGIC

# COMMAND ----------


def extract_text_to_dataframe(df, url_column, output_column):
    for index, row in df.iterrows():
        url = row[url_column]
        try:
            article = newspaper.Article(url)
            article.download()
            article.parse()
            text = article.text
            df.at[index, output_column] = text
        except Exception as e:
            print(f"Error processing URL {url}: {str(e)}")
    df[output_column] = df[output_column].apply(lambda x: json.dumps(x))
    return df


# COMMAND ----------

# MAGIC %md
# MAGIC PROCESS INPUT TABLE WITH COUNTRYCODE
# MAGIC

# COMMAND ----------

df.show()

# COMMAND ----------

news_data = pd.DataFrame({
    'NewsID': [1, 2, 3, 4, 5],
    'Actor1CountryCode': ['US', 'UK', 'CN', 'RU', 'IN'],
    'Actor2CountryCode': ['CA', 'DE', 'AU', 'JP', 'BR'],
    # Other columns...
})

# Sample input_table DataFrame
input_table = INPUT_TABLE

# Filter news_data based on Actor1CountryCode and Actor2CountryCode from input_table
filtered_data = news_data[
    (news_data['Actor1CountryCode'].isin(input_table['CountryCode'])) |
    (news_data['Actor2CountryCode'].isin(input_table['CountryCode']))
]

# Join the filtered_data with input_table on the CountryCode column
joined_data = filtered_data.merge(input_table, on='CountryCode', how='left')

# Display the joined data
print(joined_data)

# COMMAND ----------

# MAGIC %md
# MAGIC EXTRACT FULL TEXT OF NEWS ARTICLES
# MAGIC

# COMMAND ----------

extract_text_to_dataframe(joined_data, 'ArticleUrl', 'NewsText')


# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC
