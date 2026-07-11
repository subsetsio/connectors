# Representative fetch targets for api.met.no point-forecast products.
#
# The WeatherAPI forecast products (locationforecast, nowcast, oceanforecast,
# airqualityforecast, subseasonal, sunrise) are queried by lat/lon — there is
# no enumerable entity universe inside a product, so we pull a fixed, curated
# set of locations. These lists ARE the location dimension of each published
# forecast table; extend them to widen coverage.

# Populated places across mainland Norway + Svalbard (name, lat, lon).
LAND_LOCATIONS = [
    ("Oslo", 59.9139, 10.7522),
    ("Bergen", 60.3913, 5.3221),
    ("Trondheim", 63.4305, 10.3951),
    ("Stavanger", 58.9700, 5.7331),
    ("Tromso", 69.6492, 18.9553),
    ("Drammen", 59.7440, 10.2045),
    ("Kristiansand", 58.1467, 7.9956),
    ("Fredrikstad", 59.2181, 10.9298),
    ("Sandnes", 58.8524, 5.7352),
    ("Alesund", 62.4722, 6.1495),
    ("Bodo", 67.2804, 14.4049),
    ("Sarpsborg", 59.2839, 11.1096),
    ("Skien", 59.2096, 9.6090),
    ("Haugesund", 59.4138, 5.2680),
    ("Tonsberg", 59.2674, 10.4076),
    ("Arendal", 58.4616, 8.7724),
    ("Hamar", 60.7945, 11.0680),
    ("Molde", 62.7375, 7.1591),
    ("Lillehammer", 61.1153, 10.4662),
    ("Narvik", 68.4385, 17.4272),
    ("Alta", 69.9689, 23.2717),
    ("Gjovik", 60.7957, 10.6915),
    ("Mo i Rana", 66.3128, 14.1428),
    ("Kirkenes", 69.7273, 30.0450),
    ("Longyearbyen", 78.2232, 15.6267),
]

# Offshore points in the seas api.met.no oceanforecast covers (Northwestern
# Europe): North Sea, Norwegian Sea, Barents Sea, Skagerrak (name, lat, lon).
SEA_LOCATIONS = [
    ("Ekofisk", 56.5000, 3.2000),
    ("Skagerrak", 58.0000, 10.0000),
    ("Bergen offshore", 60.3000, 4.5000),
    ("Halten bank", 64.5000, 8.0000),
    ("Norwegian Sea", 65.0000, 7.0000),
    ("Lofoten offshore", 68.0000, 12.0000),
    ("Tromsoflaket", 71.0000, 19.0000),
    ("Barents Sea", 74.0000, 30.0000),
    ("Statfjord", 61.2000, 1.8000),
    ("North Sea central", 57.5000, 2.0000),
]
