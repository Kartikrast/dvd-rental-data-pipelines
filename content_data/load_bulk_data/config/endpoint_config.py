endpoint_config = {
    "base_url": "https://api.themoviedb.org/3",
    "endpoints":{
        "discover":{
            "movies":{
                "path": "/discover/movie",
                "bq_table":"raw_movies",
                "headers": {
                    "Accept": "application/json"
                },
                "params": {
                    "include_adult": True,
                    "include_video": True,
                    "page": "{{page}}",
                    "primary_release_date.gte": "{{start_date}}",
                    "primary_release_date.lte": "{{end_date}}",
                    "api_key": "{{tmdb_api_key}}"
                }
            },
            "tv_shows":{
                "path": "/discover/tv",
                "bq_table":"raw_tv_shows",
                "headers": {
                    "Accept": "application/json"
                },
                "params": {
                    "include_adult": True,
                    "include_video": True,
                    "page": "{{page}}",
                    "first_air_date.gte": "{{start_date}}",
                    "first_air_date.lte": "{{end_date}}",
                    "api_key": "{{tmdb_api_key}}"
                }
            }
        },
        "genre":{
            "movies":{
                "path": "/genre/movie/list",
                "headers":{
                    "Accept":"application/json"
                },
                "params":{
                    "api_key": "{{tmdb_api_key}}",
                    "language": "en"
                }
            },
            "tv_shows":{
                "path": "/genre/tv/list",
                "headers":{
                    "Accept":"application/json"
                },
                "params":{
                    "api_key": "{{tmdb_api_key}}",
                    "language": "en"
                }
            }
        },
        "details":{
            "movies":{
                "path": "/movie",
                "headers":{
                    "Accept":"application/json"
                },
                "params":{
                    "api_key": "{{tmdb_api_key}}"
                }
            },
            "tv_shows":{
                "path": "/tv",
                "headers":{
                    "Accept":"application/json"
                },
                "params":{
                    "api_key": "{{tmdb_api_key}}"
                }
            }
        }
    }
}