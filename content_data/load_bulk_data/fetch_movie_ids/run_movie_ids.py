"""
This file contains the functionality to handle the batch processing of the ELT Pipeline
to fetch movie_ids for the whole given year from TMDB.

This file will use the methods of `MovieIDs` class from the `movie_ids` module.
"""

# external imports
import time
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor

# local imports
from .movie_ids import MovieIDs
from ...base_log import Logger 

logger = Logger('run_movie_ids').get_logger()

class RunMovieIDs:
    def __init__(self, year:int) -> None:
        self.year = year
        self.date_ranges = self._get_date_ranges()
    
    def _get_date_ranges(self) -> List[Tuple[str, str]]:
        year = self.year
        date_ranges = [
            (f"{year}-01-01", f"{year}-01-31"),
            (f"{year}-02-01", f"{year}-02-28"),
            (f"{year}-03-01", f"{year}-03-31"),
            (f"{year}-04-01", f"{year}-04-30"),
            (f"{year}-05-01", f"{year}-05-31"),
            (f"{year}-06-01", f"{year}-06-30"),
            (f"{year}-07-01", f"{year}-07-31"),
            (f"{year}-08-01", f"{year}-08-31"),
            (f"{year}-09-01", f"{year}-09-30"),
            (f"{year}-10-01", f"{year}-10-31"),
            (f"{year}-11-01", f"{year}-11-30"),
            (f"{year}-12-01", f"{year}-12-31")
        ]
        return date_ranges


    def fetch_yearly_data(self) -> List:
        """
        Fetch movies data for multiple date ranges.
        """
        all_movies = []
        for start_date, end_date in self.date_ranges:
            logger.info(f"Fetching movies from {start_date} to {end_date}")
            obj = MovieIDs(start_date=start_date, end_date=end_date)

            # Step-1: Fetch total pages
            total_pages = obj.get_total_pages()
            
            if total_pages >= 500:
                logger.error(f"Total pages {total_pages} exceeds the limit of 500. Skipping Date Range: {start_date} to {end_date}")
                continue
            logger.info(f"Total pages to fetch: {total_pages}")
            
            # Step-2: Fetch movies data
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(MovieIDs(page=page, start_date=start_date, end_date=end_date).fetch_movies) for page in range(1, total_pages + 1)]
                count = 0
                for future in futures:
                    try:
                        movies = future.result()
                        all_movies.extend(movies)
                        time.sleep(0.5)
                        count += 1  # Sleep to avoid hitting API rate limits
                        logger.info(f"Fetched {len(movies)} movies on page {count}")
                    except Exception as e:
                        count += 1
                        logger.error(f"Error on page {count} fetching movies: {e}")
            
        if all_movies:
            movie_ids_list = []
            for movie in all_movies:
                id = movie.get("id")
                movie_ids_list.append(id)
        return movie_ids_list




if __name__ == "__main__":
    year = 2024
    """Step-1: Fetch movie_ids for the year 2024"""
    obj = RunMovieIDs(year=year)
    movie_ids = obj.fetch_yearly_data()