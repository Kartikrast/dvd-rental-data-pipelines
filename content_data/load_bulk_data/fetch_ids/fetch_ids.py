"""
This file contains the functionality to fetch ids of movies or tv_shows from TMDB.

It contains global constants:
    - `CONFIG`: Configuration object to access BigQuery and TMDB settings.
"""

# external imports
import requests
from dotenv import load_dotenv
from typing import List, Dict, Any

# local imports
from ...base_log import Logger
from ..config.config import Config
load_dotenv()

CONFIG = Config()
logger = Logger('fetch_ids').get_logger()

class FetchIDs:
    """
    This class contains methods to fetch movie and tv_show ids from TMDB.
    It uses the Config() module to access configuration and endpoint settings for TMDB.
    It sets configurations as follows:

        - `self.url`: TMDB API endpoint for fetching ids.
        - `self.headers`: TMDB API headers.
        - `self.default_params`: TMDB API default parameters.
        - `self.page`: Page number for fetching ids.
        - `self.start_date`: Start date for fetching ids.
        - `self.end_date`: End date for fetching ids.
        - `self.type`: This will tell the program which ids to fetch (movies or tv_shows). Defaults to `movies`.
        - `self._set_params()`: Sets the parameters for fetching ids.
        - `self.total_page_params`: Parameters for fetching total pages.
        - `self.dynamic_params`: Parameters for fetching ids dynamically.
    
    #### Notes:

        - The class relies on a Config helper (`config.Config`) to supply TMDB endpoint details, keeping secrets out of the source code.
    
    #### Example Usage:

        >>> raw_movies = FetchIDs(page=1, start_date="2020-01-01", end_date="2020-12-31", type="movies")
        >>> total_pages = raw_movies.get_total_pages()
        >>> movies = raw_movies.fetch_ids()
    """
    def __init__(self, page: int = None, start_date: str = None, end_date: str = None, type:str = "movies"):
        self.type = type
        self.url, self.headers, self.default_params = CONFIG.get_tmdb_config(endpoint="discover", type=self.type)
        self.page = page
        self.start_date = start_date
        self.end_date = end_date
        self._set_params()
    
    def _set_params(self):
        """
        Set the parameters for fetching movies.

        Args:
            page (int): Page number for fetching movies.
            start_date (str): Start date for fetching movies.
            end_date (str): End date for fetching movies.
        """
        if self.type == "movies":
            self.total_page_params = {
                "page":1,
                "primary_release_date.gte": self.start_date,
                "primary_release_date.lte": self.end_date
            }

            self.dynamic_params = {
                "page": self.page,
                "primary_release_date.gte": self.start_date,
                "primary_release_date.lte": self.end_date
            }
        elif self.type == "tv_shows":
            self.total_page_params = {
                "page":1,
                "first_air_date.gte": self.start_date,
                "first_air_date.lte": self.end_date
            }

            self.dynamic_params = {
                "page": self.page,
                "first_air_date.gte": self.start_date,
                "first_air_date.lte": self.end_date
            }
    
    def get_total_pages(self) -> int:
        """
        Get the total number of pages for the given date range.
        
        Returns:
            int: Total number of pages.
        
        Examples:

            >>> movie_ids = FetchIDs(page=1, start_date="2020-01-01", end_date="2020-12-31")
            >>> total_pages = movie_ids.get_total_pages()
            >>> tv_show_ids = FetchIDS(page=1, start_date="2020-01-01", end_date="2020-12-31", type="tv_shows")
            >>> total_pages = tv_show_ids.get_total_pages()
        """
        url = self.url
        params = CONFIG.set_tmdb_params(params=self.default_params, **self.total_page_params)
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('total_pages', 1)
        else:
            logger.error(f"Failed to fetch total pages: {response.status_code} - {response.text}")
            raise Exception(f"Failed to fetch total pages: {response.status_code} - {response.text}")
    
    def fetch_ids(self) -> List[Dict[str, Any]]:
        """
        Fetch ids from TMDB.
        
        Returns:

            List[Dict[str, Any]]: List of ids having metadata.
        
        Examples:
        
            >>> movie_ids = FetchIDs(page=1, start_date="2020-01-01", end_date="2020-12-31")
            >>> ids = movie_ids.fetch_ids()
            >>> tv_show_ids = FetchIDS(page=1, start_date="2020-01-01", end_date="2020-12-31", type="tv_shows")
            >>> ids = tv_show_ids.fetch_ids()
        """
        url = self.url
        params = CONFIG.set_tmdb_params(params=self.default_params, **self.dynamic_params)
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            logger.error(f"Failed to fetch data: {response.status_code} - {response.text}")
            raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")