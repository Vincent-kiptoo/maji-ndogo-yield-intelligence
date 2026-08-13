"""
This module handles database connections, SQL query execution and csv file reading from web sources.
Provides utilities for loading agricultural data from multiple sources into the pipeline
"""

from sqlalchemy import create_engine, text, Engine
import pandas as pd
from src.logging_config import get_logger

logger = get_logger(__name__)

logger.info("Starting data ingestion")

def create_db_engine(db_path, echo = False) -> Engine:
    """
    Creates a SQLAlchemy engine
    """
    try:
        engine = create_engine(db_path, echo = echo)

        with engine.connect() as connection:
            result = connection.execute(text("Select 1"))
            result.fetchone()

        logger.info(f"Successfully connected to {db_path}")
        return engine

    except ImportError:
        logger.error("SQL alchemy is not imported. Please import sql alchemy using pip install sqlalchemy")
        raise
    except Exception  as e:
        logger.error(f"The database connection failed: {e}")
        raise ConnectionError(f"Failed to connect to the database: {e}") from e

def query_data(engine, sql_query, allow_empty = False) -> pd.DataFrame:
    """
    Executes the sql query and returns the sql query results as a pandas DataFrame
    """
    try:
        with engine.connect() as connection:
            df = pd.read_sql_query(text(sql_query), connection)
    except Exception as e:
        logger.error(f"Query execution failed: {e}") 
        raise

    if df.empty and not allow_empty:
        msg = f"Query returned no results: {sql_query[:100]}..."
        logger.error(msg)
        raise ValueError(msg)

    logger.info(f"Query executed successfully. Rows: {len(df)}")
    return df

def read_from_web_CSV(URL) -> pd.DataFrame:
    """
    Fetches externel weather and survey datasets used in the maji ndogo pipeline
    """

    if not URL or not isinstance(URL, str):
        error_msg = f"Invalid URL provided: {URL}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    try:
        logger.info(f"Attempting to read CSV from: {URL}")
        df = pd.read_csv(URL)
        if df.empty:
            error_msg = f"CSV file is empty: {URL}"
            logger.warning(error_msg)
            raise pd.errors.EmptyDataError(error_msg)
        logger.info(f"Successfully read CSV: {len(df)} rows, {len(df.columns)} columns")
        return df
    except pd.errors.EmptyDataError as e:
        logger.error(f"CSV file is empty: {URL}")
        raise
    except pd.errors.ParserError as e:
        logger.error(f"failed to purse CSV from {URL}. Error: {e}")
        raise
    except Exception as e:
        logger.error(f"FAiled to read csv from {URL}. Error {e}")
        raise Exception(f"Could not read CSV from {URL}. Check you internet connection. Error {e}")
    
