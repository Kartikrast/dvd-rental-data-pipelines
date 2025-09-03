"""
This file contains the functionality to handle the batch processing of the ELT Pipeline
to fetch the movie details data from TMDB.
This file is created to fetch the data in bulk using asyncio.

This file will use the methods of `MovieDetails` class from the `movie_details` module to fetch the movie details data from TMDB.
"""

# external imports
import httpx
import asyncio
from typing import List, Dict, Any
import os
import json


# local imports
from .movie_details import MovieDetails
from ...base_log import Logger

logger = Logger('run_movie_details').get_logger()

class RunMovieDetails:
    def __init__(self, movie_ids: List[int]) -> None:
        self.movie_ids = movie_ids
        self.semaphore = asyncio.Semaphore(10)

    async def fetch_all_movies(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(limits=httpx.Limits(max_connections=200, max_keepalive_connections=50)) as client:
            tasks = [
                self._fetch_movie(movie_id, client) for movie_id in self.movie_ids
            ]
            return await asyncio.gather(*tasks)

    async def _fetch_movie(self, movie_id: int, client: httpx.AsyncClient) -> Dict[str, Any]:
        async with self.semaphore:  # limit concurrency
            movie = MovieDetails(movie_id=movie_id, client=client)
            return await movie.get_complied_data()

    async def main(self):
        results = await self.fetch_all_movies()
        return results

    

if __name__ == "__main__":
    # import pandas as pd
    # movie_ids = pd.read_csv(r"C:\Users\karti\Documents\dvd_rental\data\temp\movies_id.csv")["id"].tolist()
    movie_ids = [155]
    
    obj = RunMovieDetails(movie_ids=movie_ids)
    movies = asyncio.run(obj.main())
    
    # # let's store this data into a json file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "movie_details.json")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write('{"results": ')
        json.dump(movies, f, indent=4)
        f.write('}')