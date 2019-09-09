# weather.inplaces

Simple app that prompts users for a location and returns weather data for that location.

Demo here: https://weather-in-places.herokuapp.com/weather/

App runs on Django and uses Dark Sky API to pull weather info. API does have 1000 a day limit. Locations are converted to lat, long using geopy. Database is PostgreSQL, which I migrated from SQLite when I found out heroku doesn't support it :)

I had never used Django, nor really spent time in a relational database, so this was a great dive into web dev. Settings.py and a few other places got a bit sloppy as I tried to troubleshoot issues with heroku deployment--which ended up being a series of edge cases like a static file not having anything in it and so not getting added to git... 

