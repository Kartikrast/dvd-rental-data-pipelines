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
from .fetch_ids import FetchIDs
from ...base_log import Logger 

logger = Logger('run_fetch_ids').get_logger()

class RunFetchIDs:
    def __init__(self, year:int, type:str = "movies") -> None:
        self.type = type
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
        Fetch ids for multiple date ranges.
        """
        all_ids = []
        for start_date, end_date in self.date_ranges:
            logger.info(f"Fetching ids from {start_date} to {end_date}")
            obj = FetchIDs(start_date=start_date, end_date=end_date, type=self.type)

            # Step-1: Fetch total pages
            total_pages = obj.get_total_pages()
            
            if total_pages >= 500:
                logger.error(f"Total pages {total_pages} exceeds the limit of 500. Skipping Date Range: {start_date} to {end_date}")
                continue
            logger.info(f"Total pages to fetch: {total_pages}")
            
            # Step-2: Fetch ids
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(FetchIDs(page=page, start_date=start_date, end_date=end_date, type=self.type).fetch_ids) for page in range(1, total_pages + 1)]
                count = 0
                for future in futures:
                    try:
                        ids = future.result()
                        all_ids.extend(ids)
                        time.sleep(0.5)
                        count += 1  # Sleep to avoid hitting API rate limits
                        logger.info(f"Fetched {len(ids)} ids on page {count}")
                    except Exception as e:
                        count += 1
                        logger.error(f"Error on page {count} fetching ids: {e}")
            
        if all_ids:
            ids_list = []
            for data in all_ids:
                id = data.get("id")
                ids_list.append(id)
        return ids_list




if __name__ == "__main__":
    year = 2024
    """Step-1: Fetch movie_ids for the year 2024"""
    obj = RunFetchIDs(year=year, type="tv_shows")
    ids = obj.fetch_yearly_data()