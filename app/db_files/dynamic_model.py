from sqlalchemy import text
from sqlalchemy import MetaData
import pandas as pd
from loguru import logger

metadata = MetaData()


def execute_query_to_df(session, query: str):
    try:
        result = session.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df
    except Exception as e:
        logger.error(e)
        return None
