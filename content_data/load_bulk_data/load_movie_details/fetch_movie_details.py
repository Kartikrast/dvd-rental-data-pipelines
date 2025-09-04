"""
This file contains the functionality to fetch all the movie details from TMDB
as the part of ELT pipeline.

It contains global constants:
    - `CONFIG`: Configuration object to access MongoDB and TMDB settings.
"""

# external imports
import httpx
import asyncio
import random
from dotenv import load_dotenv
from typing import Dict, Any
load_dotenv()

# local imports
from ..config.config import Config
from ...base_log import Logger

logger = Logger('run_movie_details').get_logger()
CONFIG = Config()

class MovieDetails:
    """
    This class contains the methods to fetch movie details from TMDB.
    It uses asyncio to fetch movie details so that the fetching time can be optimized.

    A helper method is used in this class which will help to frame the api request url for different endpoints such as:
        - `details`
        - `credits`
        - `images`
        - `videos`
    This method is called `_fetch` and it takes an optional `endpoint` parameter.

    The following async methods are used to fetch the data from TMDB for different endpoints:-
        - `fetch_movie_details`
        - `fetch_movie_credits`
        - `fetch_movie_images`
        - `fetch_movie_videos`
    These methods are called in the `get_complied_data` method and the data is stored in a dictionary with all the details combined.

    This is the framing module for each of the details we need for a single move. 
    This module is a backbone of the `run_movie_details` file which will fetch multiple movie details asynchronously.
    
    #### Notes:
        - This class relies on a Config helper (`config.Config`) to supply TMDB endpoint details,
        keeping secrets out of the source code.
    
    #### See Also:
        - `endpoint_config.py` – maps TMDB endpoint types to paths.
    """
    def __init__(self, movie_id:int=None, client: httpx.AsyncClient=None) -> None:
        self.url, self.headers, self.default_params = CONFIG.get_tmdb_config(endpoint="details", type="movies")
        self.movie_id = movie_id
        self.client = client
    
    async def _fetch(self, endpoint: str = "") -> Dict[str, Any]:
        url = f"{self.url}/{self.movie_id}{endpoint}"
        params = CONFIG.set_tmdb_params(params=self.default_params)
        retries = 3
        backoff = 1

        for attempt in range(1, retries + 1):
            try:
                response = await self.client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                logger.info(f"✅ Successfully fetched {endpoint}/details of movie_id: {self.movie_id} (attempt {attempt})")
                return response.json()

            except Exception as e:
                logger.warning(f"⚠️ Attempt {attempt} failed for movie_id={self.movie_id}: {e}")
                if attempt == retries:
                    logger.error(f"❌ Giving up after {retries} attempts for movie_id={self.movie_id}")
                    return None
                sleep_time = backoff * 2 ** (attempt - 1) + random.uniform(0, 0.5)
                await asyncio.sleep(sleep_time)
    
    async def fetch_movie_details(self) -> Dict[str, Any]:
        return await self._fetch()
    
    async def fetch_movie_credits(self) -> Dict[str, Any]:
        return await self._fetch("/credits")
    
    async def fetch_movie_images(self) -> Dict[str, Any]:
        return await self._fetch("/images")
    
    async def fetch_movie_videos(self) -> Dict[str, Any]:
        return await self._fetch("/videos")
        
    async def get_complied_data(self) -> Dict[str, Any]:
        details, credits, images, videos = await asyncio.gather(
            self.fetch_movie_details(),
            self.fetch_movie_credits(),
            self.fetch_movie_images(),
            self.fetch_movie_videos(),
        )
        try:
            mapping ={
                "id": details.get("id"),
                "details": details,
                "credits": credits,
                "images": images,
                "videos": videos
            }
            return mapping
        except Exception as e:
            logger.error(f"❌ Error fetching movie details: {e}")
            return None