import pandas as pd
from langchain.text_splitter import CharacterTextSplitter

def split_text_into_chunks(
        input_df: pd.DataFrame,
        content_col:str,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
        separator:str = " ",
        chunk_colname : str='Chunk_Number',
    ) -> pd.DataFrame:
    """Split the content of a DataFrame into chunks of a given size.

    Args:
        input_df (pd.DataFrame): The DataFrame containing the content to be chunked.
        content_col (str): The name of the column containing the content to be chunked.
        chunk_size (int): The size of each chunk.
        chunk_overlap (int): The number of characters to overlap between chunks.
        separator (str): The separator to use when splitting the content.
        chunk_colname (str): The name of the column to store the chunk number.

    Returns:
        pd.DataFrame: A new DataFrame containing the chunked content.
    """
    splitter = CharacterTextSplitter(separator=separator, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunked_data = {col: [] for col in input_df.columns}
    chunked_data[chunk_colname] = []
    for _, row in input_df.iterrows():
        chunks = splitter.split_text(row[content_col])
        for i, chunk in enumerate(chunks, start=1):
            for col in input_df.columns:
                chunked_data[col].append(row[col])
            chunked_data[content_col][-1] = chunk
            chunked_data[chunk_colname].append(i)
    return pd.DataFrame(chunked_data).reset_index(drop=True).reset_index().rename(columns={'index': 'ID'})