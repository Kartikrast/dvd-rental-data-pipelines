"""
This file contains the functionality to fetch and load yearly data from TMDB.
"""

import os
import sys
import asyncio
import json
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

from content_data import Config, Logger, RunMovieDetails, RunFetchIDs

config = Config()
db = config.get_mongo_db()
movie_collection = db['movies']
image_collection = db['images']
video_collection = db['videos']
people_collection = db['people']


def get_ids(year, type:str="movies"):
    obj = RunFetchIDs(year=year, type=type)
    ids = obj.fetch_yearly_data()
    return ids

def get_movie_details(movie_ids):
    obj = RunMovieDetails(movie_ids=movie_ids)
    movies = asyncio.run(obj.main())
    return movies

def format_movie_data(movies):
    details = []
    credits = []
    images = []
    videos = []
    for index, movie in enumerate(movies):
        try:
            details.append(movie.get('details'))
            credits.append(movie.get('credits'))
            images.append(movie.get('images'))
            videos.append(movie.get('videos'))
        except:
            print(index)
    return details, credits, images, videos

def load_details(details, year):
    filtered_docs = []
    allowed_keys = [
        'id', 'title', 'adult', 'backdrop_path', 'poster_path',
        'release_date', 'release_year', 'overview', 'tagline',
        'runtime', 'genres', 'cast', 'director', 'production_companies',
        'popularity', 'vote_average', 'vote_count', 'status',
        'original_language', 'production_countries', 'budget', 'revenue', 'trailer'
    ]

    for detail in details:
        detail['release_year'] = year

        # Fetch full video doc for this movie
        video_doc = video_collection.find_one({"id": detail["id"]})

        trailer = None
        if video_doc and "results" in video_doc:
            # Search manually for the trailer inside results
            for v in video_doc["results"]:
                if v.get("type") == "Trailer":
                    trailer = v
                    break

        # Filter fields from details
        filtered_doc = {k: detail.get(k) for k in allowed_keys if k in detail}
        filtered_doc["trailer"] = trailer
        filtered_docs.append(filtered_doc)

    if filtered_docs:
        movie_collection.insert_many(filtered_docs)

    print(f"✅ Inserted {len(filtered_docs)} movies for year:{year}")
    return

def load_images(images, year):
    fixed_docs = []
    for index, doc in enumerate(images):
        try:
            transformed = {k: v for k, v in doc.items() if k != "id"}

            transformed["movie_id"] = doc["id"]

            fixed_docs.append(transformed)
        except:
            print(index)

    # Insert into MongoDB
    if fixed_docs:
        image_collection.insert_many(fixed_docs)
    print(f"✅ Inserted {len(fixed_docs)} images for year:{year}.")
    return

def load_videos(videos, year):
    video_collection.insert_many(videos)
    print(f"✅ Inserted {len(videos)} videos for year:{year}")


script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, 'fetch_year.json')
with open(json_path, mode='r', encoding='utf-8') as f:
    file = json.load(f)
    year = file["year"]
    print(f"Fetching for year: {year}")

ids = get_ids(year)
movies = get_movie_details(ids)
details, credits, images, videos = format_movie_data(movies)
input("Please turn off VPN and hit enter!")
load_details(details, year)
load_images(images, year)
load_videos(videos, year)

with open(json_path, mode='w', encoding='utf-8') as f:
    year_dict = {
        "year":year-1
    }
    json.dump(year_dict, f)
    print(f"Updated json with year: {year}")

