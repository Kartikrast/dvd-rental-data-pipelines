"""
This module contains configuration settings to fetch Data from TMDB.
"""

# imports
import os
from copy import deepcopy
from dotenv import load_dotenv
from typing import Tuple, Dict, Any
from pymongo import MongoClient
from pymongo.database import Database
load_dotenv()

# local imports
from .endpoint_config import endpoint_config


class Config:
    """
    Configuration class for fetching data from TMDB.
    This class loads environment variables,
    and provides methods to load TMDB configurations.
    
    To load the TMDB endpoint configuration for a specific endpoint and type, use:meth:`get_tmdb_config`::

        endpoint = "discover"
        type = "movies"
        url, headers, params = config.get_tmdb_config(endpoint, type)
    """


    def __init__(self) -> None:
        self.tmdb_api_key = os.getenv("TMDB_API_KEY")
        self.mongo_username = os.getenv("MONGO_USER")
        self.mongo_password = os.getenv("MONGO_PASSWORD")
        self.mongo_host = os.getenv("MONGO_HOST")
        self.mongo_port = int(os.getenv("MONGO_PORT"))
        self.mongo_db = os.getenv("MONGO_DB")

        required_vars = {
            "TMDB_API_KEY": self.tmdb_api_key
        }

        missing = [var for var, value in required_vars.items() if not value]
        if missing:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")
    
    def get_tmdb_config(self, endpoint:str, type:str) -> Tuple[str, Dict[str, str], Dict[str, Any]]:
        """
        Retrieves the TMDB API endpoint configuration 
        for a given endpoint and type (e.g., "movies" or "tv_shows").
        This method returns the url, headers and parameters required 
        to make a request to the TMDB API.
        
        **NOTE: The parameters:meth:`params` are required to be filled with the 
        appropriate values before making the request.**

        To get the schema and partitioning information use::

            config = Config()
            schema, partition_field, partition_type = config.load_bq_schema("table_name_here")
        """
        base_url = endpoint_config["base_url"]

        endpoint_type = endpoint_config["endpoints"][endpoint][type]
        endpoint_path = endpoint_type.get("path")

        if not endpoint_path:
            raise ValueError(f"Endpoint {endpoint} not found in endpoint configuration.")
        
        url = f"{base_url}{endpoint_path}"

        headers = endpoint_type.get("headers")

        params = endpoint_type.get("params", {})

        params["api_key"] = self.tmdb_api_key
        return url, headers, params
    

    # helper method to set the params for making the API request
    def set_tmdb_params(self, params: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        This is a helper method, it sets the parameters dynamically for the TMDB API request.
        This method updates the `params` dictionary with additional keyword arguments.

        To set the parameters use::

            config = Config()
            url, headers, params = config.get_tmdb_config("discover", "movies")
            updated_params = config.set_tmdb_params(params=params, **{
                "param_key": "updated_value"
            })
        """
        updated_params = deepcopy(params)
        updated_params.update(kwargs)
        return updated_params
    
    # method to get the mongoDB client
    def get_mongo_db(self) -> Database:
        """
        This method provides us with the Database object of the MongoDB,
        in which we want to store the content data keeping the environment variables
        out of the source code.

        In order to get the database object, make sure you have set these environment variables
        in a .env file:-
            ```
            MONGO_USER=<your_mongoDB_user>
            MONGO_PASSWORD=<your_mongoDB_password>
            MONGO_HOST=<your_mongoDB_host>
            MONGO_PORT=<your_mongoDB_port>
            MONGO_DB=<your_mongoDB_db>
            ```

        To get the database use::

            config = config()
            db = config.get_mongo_db()
        """
        connection_string = f"mongodb://{self.mongo_username}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}/{self.mongo_db}"
        client = MongoClient(connection_string)
        db = client[self.mongo_db]
        return db







if __name__ == "__main__":
    config = Config()
    url, headers, params = config.get_tmdb_config("discover", "movies")
    db = config.get_mongo_db()
    collections = db.list_collection_names()
    print("Collections:", collections)