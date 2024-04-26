import pandas as pd
import json
import newspaper

def extract_text_to_dataframe(df, url_column, output_column):
    for index, row in df.iterrows():
        url = row[url_column]
        try:
            article_obj = newspaper.Article(url)
            article_obj.download()
            article_obj.parse()
            text = article_obj.text
            df.at[index, output_column] = text

        except Exception as e:
            print(f"Error processing URL {url}: {str(e)}")
            df.at[index, output_column] = ""  # Assign an empty string or any default value if there's an error
    df[output_column] = df[output_column].apply(lambda x: json.dumps(x)).fillna("")
    return df
