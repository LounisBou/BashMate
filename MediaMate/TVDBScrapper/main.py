#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import tvdb_v4_official

tvdb = tvdb_v4_official.TVDB("b6d9d9cb-1c6e-4f47-a032-00c5ae8b666f")
# OR:
# tvdb = tvdb_v4_official.TVDB("APIKEY", pin="YOUR PIN HERE")

# fetching several pages of series info
series_list = [ ]
for j in range(5): # Pages are numbered from 0
    series_list += tvdb.get_all_series(j)

# fetching a series
series = tvdb.get_series(121361)

# fetching a season's episode list
series = tvdb.get_series_extended(121361)
for season in sorted(series["seasons"], key=lambda x: (x["type"]["name"], x["number"])):
    if season["type"]["name"] == "Aired Order" and season["number"] == 1:
        season = tvdb.get_season_extended(season["id"])
        break
    else:
        season = None
        
if season is not None:
    print(season["episodes"])

# fetch a page of episodes from a series by season_type (type is "default" if unspecified)
info = tvdb.get_series_episodes(121361, page=0)
print(info["series"])
for ep in info["episodes"]:
    print(ep)

# fetching a movie
movie = tvdb.get_movie(31) # avengers

# access a movie's characters
movie = tvdb.get_movie_extended(31)
for c in movie["characters"]:
    print(c)

# fetching a person record
person = tvdb.get_person_extended(characters[0]["peopleId"])
print(person)

# using since If-Modifed-Since parameter
series = tvdb.get_series_extended(393199, if_modified_since="Wed, 30 Jun 2022 07:28:00 GMT")