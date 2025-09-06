## people
```
db.createCollection("people", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: [ "id", "name" ],
            properties: {
                id: {
                    bsonType: "int",
                    description: "TMDB person_id. Must be an integer and is required."
                },
                name: {
                    bsonType: "string",
                    description: "Name of the person. Must be a string and is required."
                },
                known_for_department: {
                    bsonType: "string",
                    description: "Primary department the person is known for."
                },
                biography: {
                    bsonType: "string",
                    description: "Biography of the person."
                },
                birthday: {
                    bsonType: ["date", "null"],
                    description: "Person's date of birth."
                },
                deathday: {
                    bsonType: ["date", "null"],
                    description: "Person's date of death."
                },
                gender: {
                    bsonType: "int",
                    "enum": [0, 1, 2, 3],
                    description: "Gender of the person. Must be 0, 1, 2, or 3 if provided."
                },
                place_of_birth: {
                    bsonType: ["string", "null"],
                    description: "Place of birth."
                },
                profile_path: {
                    bsonType: ["string", "null"],
                    description: "Path to the profile image."
                },
                imdb_id: {
                    bsonType: ["string", "null"],
                    description: "IMDB ID for the person."
                },
                popularity: {
                    bsonType: "double",
                    description: "Popularity score from TMDB."
                }
            }
        }
    },
    validationLevel: "strict",
    validationAction: "error"
});
```

## Images
```
db.createCollection("images", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: [ "movie_id"],
            properties: {
                movie_id: {
                    bsonType: "int",
                    description: "The TMDB movie id this image belongs to. Links to movies.id. Required."
                },
                type: {
                    bsonType: "string",
                    "enum": [ "posters", "backdrops", "logos" ],
                    description: "The type of image. Must be 'posters', 'backdrops', or 'logos'. Required."
                },
                data: {
                    bsonType: "array",
                    description: "An array of image objects. Required.",
                    items: {
                        bsonType: "object",
                        required: [ "file_path" ],
                        properties: {
                            file_path: {
                                bsonType: "string",
                                description: "The path part of the full image URL. Required."
                            },
                            width: {
                                bsonType: "int",
                                description: "Width of the image in pixels. Optional."
                            },
                            height: {
                                bsonType: "int",
                                description: "Height of the image in pixels. Optional."
                            },
                            aspect_ratio: {
                                bsonType: "double",
                                description: "Aspect ratio of the image. Optional."
                            },
                            vote_average: {
                                bsonType: "double",
                                description: "Average vote score for this image. Optional."
                            },
                            vote_count: {
                                bsonType: "int",
                                description: "Number of votes for this image. Optional."
                            },
                            iso_639_1: {
                                bsonType: [ "string", "null" ],
                                description: "Language code for this image variant (e.g., 'en'). Optional."
                            }
                        }
                    }
                }
            }
        }
    },
    validationLevel: "strict",
    validationAction: "error"
});
```

## Videos
```
db.createCollection("videos", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: [ "movie_id", "videos" ],
            properties: {
                movie_id: {
                    bsonType: "int",
                    description: "The TMDB movie id this video belongs to. Links to movies.id. Required."
                },
                videos: {
                    bsonType: "array",
                    description: "An array of video objects. Required.",
                    items: {
                        bsonType: "object",
                        required: [ "id", "key", "site", "type", "name" ],
                        properties: {
                            id: {
                                bsonType: "string",
                                description: "Unique identifier for the video from the source (e.g., TMDB). Required."
                            },
                            key: {
                                bsonType: "string",
                                description: "The key used to construct the video URL (e.g., YouTube video ID). Required."
                            },
                            name: {
                                bsonType: "string",
                                description: "The title/name of the video. Required."
                            },
                            site: {
                                bsonType: "string",
                                description: "The hosting platform. Must be 'YouTube' or 'Vimeo'. Required."
                            },
                            type: {
                                bsonType: "string",
                                description: "The category of the video. Required."
                            },
                            size: {
                                bsonType: "int",
                                description: "The resolution of the video (e.g., 1080). Optional."
                            },
                            official: {
                                bsonType: "bool",
                                description: "Indicates if the video is an official release. Optional."
                            },
                            published_at: {
                                bsonType: "date",
                                description: "The date the video was published. Optional."
                            }
                        }
                    }
                }
            }
        }
    },
    validationLevel: "strict",
    validationAction: "error"
});
```

## Movie
```
db.createCollection("movies", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["id", "title", "release_date"],
            properties: {
                id: {
                    bsonType: "int",
                    description: "The TMDB movie id. Must be a unique integer. Required."
                },
                title: {
                    bsonType: "string",
                    description: "The title of the movie. Required."
                },
                adult: {
                    bsonType: "bool",
                    description: "Indicates if the movie is adult content."
                },
                backdrop_path: {
                    bsonType: ["string", "null"],
                    description: "Path to the backdrop image. Can be null."
                },
                poster_path: {
                    bsonType: ["string", "null"],
                    description: "Path to the poster image. Can be null."
                },
                release_date: {
                    bsonType: ["date", "null"],
                    description: "Theatrical release date. Can be null. Required."
                },
                release_year: {
                    bsonType: "int",
                    description: "Year derived from release_date. Used for efficient filtering. Optional but highly recommended."
                },
                overview: {
                    bsonType: ["string", "null"],
                    description: "Plot summary. Optional."
                },
                tagline: {
                    bsonType: ["string", "null"],
                    description: "The movie's tagline. Optional."
                },
                runtime: {
                    bsonType: ["int", "null"],
                    description: "Runtime in minutes. Optional."
                },
                genres: {
                    bsonType: "array",
                    description: "Array of genre objects. Optional.",
                    items: {
                        bsonType: "object",
                        required: ["id", "name"],
                        properties: {
                            id: { bsonType: "int" },
                            name: { bsonType: "string" }
                        }
                    }
                },
                cast: {
                    bsonType: "array",
                    description: "Array of top cast members (e.g., first 10). Optional.",
                    items: {
                        bsonType: "object",
                        required: ["person_id", "name", "character", "order"],
                        properties: {
                            person_id: { bsonType: "int" },
                            name: { bsonType: "string" },
                            character: { bsonType: "string" },
                            profile_path: { bsonType: ["string", "null"] },
                            order: { bsonType: "int" }
                        }
                    }
                },
                director: {
                    bsonType: ["object", "null"],
                    description: "Main director extracted from the crew. Optional.",
                    required: ["person_id", "name"],
                    properties: {
                        person_id: { bsonType: "int" },
                        name: { bsonType: "string" }
                    }
                },
                production_companies: {
                    bsonType: "array",
                    description: "Array of production company objects. Optional.",
                    items: {
                        bsonType: "object",
                        required: ["id", "name"],
                        properties: {
                            id: { bsonType: "int" },
                            name: { bsonType: "string" },
                            logo_path: { bsonType: ["string", "null"] }
                        }
                    }
                },
                popularity: {
                    bsonType: "double",
                    description: "TMDB popularity score. Optional."
                },
                vote_average: {
                    bsonType: "double",
                    description: "Average user rating. Optional."
                },
                vote_count: {
                    bsonType: "int",
                    description: "Number of user ratings. Optional."
                },
                status: {
                    bsonType: "string",
                    enum: ["Rumored", "Planned", "In Production", "Post Production", "Released", "Canceled"],
                    description: "The production status of the movie. Optional."
                },
                original_language: {
                    bsonType: "string",
                    description: "ISO 639-1 code of the original language (e.g., 'en'). Optional."
                },
                production_countries: {
                    bsonType: "array",
                    description: "Array of country objects. Optional.",
                    items: {
                        bsonType: "object",
                        required: ["iso_3166_1", "name"],
                        properties: {
                            iso_3166_1: { bsonType: "string" },
                            name: { bsonType: "string" }
                        }
                    }
                },
                budget: {
                    bsonType: "long",
                    description: "Production budget in USD. Optional."
                },
                revenue: {
                    bsonType: "long",
                    description: "Total revenue in USD. Optional."
                },
                trailer: {
                    bsonType: ["object", "null"],
                    description: "This is the video trailer of the movie. Optional."
                }
            }
        }
    },
    validationLevel: "strict",
    validationAction: "error"
})
```

## Movie IDs
```
db.createCollection("movie_ids", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["id", "year"],
            properties: {
                id: {
                    bsonType: "int"
                },
                year: {
                    bsonType: "int"
                }
            }
        }
    },
    validationLevel: "strict",
    validationAction: "error"
});
```
