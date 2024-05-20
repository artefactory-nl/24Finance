import pandas as pd
from typing import List, Dict

def build_vector_db_structure(input_df:pd.DataFrame, metadata_cols:List[str], id_col:str, text_col:str) -> Dict:
    """Build a vector database structure from a pandas DataFrame.

    Args:
        input_df (pd.DataFrame): Input DataFrame.
        metadata_cols (List[str]): List of metadata columns.
        id_col (str): ID column.
        text_col (str): Text column.
    
    Returns:
        Dict: Vector database structure.
    """
    vector_db = {
        'ids': [],
        'metadatas': [],
        'datas': []
    }
    for _, row in input_df.iterrows():
        vector_db['ids'].append(str(row[id_col]))
        vector_db['datas'].append(row[text_col])
        vector_db['metadatas'].append({col: row[col] for col in metadata_cols})
    return vector_db
