from sqlalchemy import create_engine, text
import logging
import pandas as pd

"""
Module: Data Ingestion 

This module handles the ingestion of data into the Maji Ndogo farm survey database 

Import Statements: The code imports necessary modules such as create_engine and text from SQLAlchemy, logging, and pandas for data manipulation.

Logger Configuration: It configures a logger named 'data_ingestion' using the Python logging module. 
The logger will output log messages of level INFO and above to the console with a specific format including a timestamp, logger name, and log le
"""
# Name our logger so we know that logs from this module come from the data_ingestion module
logger = logging.getLogger('data_ingestion')
# Set a basic logging message up that prints out a timestamp, the name of our logger, and the message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def create_db_engine(db_path):
    """
    Create a database engine: the function creates SQLAchemy database engine using the specified database path
    
    Args: db_path (str): The path to the database  
    
    Returns: engine (sqlalchemy.engine.Engine): The SQLAlchemy engine object. 
    
    Raises: ImportError: If SQLAlchemy is not installed.
    Exception: If there is an error creating the database engine.
    """    
    try:
        engine = create_engine(db_path)
        # Test connection
        with engine.connect() as conn:
            pass
        # test if the database engine was created successfully
        logger.info("Database engine created successfully.")
        return engine # Return the engine object if it all works well
    except ImportError: #If we get an ImportError, inform the user SQLAlchemy is not installed
        logger.error("SQLAlchemy is required to use this function. Please install it first.")
        raise e
    except Exception as e:# If we fail to create an engine inform the user
        logger.error(f"Failed to create database engine. Error: {e}")
        raise e
        
     
    
def query_data(engine, sql_query): 
    """"
    Query_data: executes a SQL query on the database engine and returns the result as a pandas DataFrame. 
    
    Args:
       engine (sqlalchemy.engine.Engine): The SQLAlchemy engine object.
       sql_query (str): The SQL query to be executed. 
       
       Returns: df (pandas.DataFrame): The result of the SQL query as a pandas DataFrame. 
       
       Raises:ValueError: if the querry returns an empty df
       Exception: if there is an error while querrying the database.
       
        """
        
    try:
        with engine.connect() as connection:
            df = pd.read_sql_query(text(sql_query), connection)
        if df.empty:
            # Log a message or handle the empty DataFrame scenario as needed
            msg = "The query returned an empty DataFrame."
            logger.error(msg)
            raise ValueError(msg)
        logger.info("Query executed successfully.")
        return df
    except ValueError as e: 
        logger.error(f"SQL query failed. Error: {e}")
        raise e
    except Exception as e:
        logger.error(f"An error occurred while querying the database. Error: {e}")
        raise e
        

def read_from_web_CSV(URL):
    """
    Read from web csv:
        reads csv file from the specified URL and retrns it as pandas dataframe
    
    Args:
        URL from where csv file is located.
    
    Returns:
        dataframe (pandas.DataFrame) with the csv data
    
    Raises:
        pd.errors.EmptyDataError if URL is not found or it is empty.
        Exception if the URL is not readable from the web or there is error whi;e reading the file from teh web
    
       
    
        """
    try:
        df = pd.read_csv(URL)
        logger.info("CSV file read successfully from the web.")
        return df
    except pd.errors.EmptyDataError as e:
        logger.error("The URL does not point to a valid CSV file. Please check the URL and try again.")
        raise e
    except Exception as e:
        logger.error(f"Failed to read CSV from the web. Error: {e}")
        raise e
    
### END FUNCTION