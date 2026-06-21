# Curation data for the Open-Meteo connector (data, not logic).
#
# Open-Meteo has no catalog endpoint: data is parameterized by latitude /
# longitude. Each published product table is therefore sampled at a fixed,
# curated set of globally distributed major cities (location is a column, not a
# per-location node). The list is biased toward cities on or near major rivers
# so the GloFAS `flood` product returns meaningful river discharge.

# name, country (ISO-ish short), latitude, longitude
LOCATIONS = [
    ("London", "United Kingdom", 51.5074, -0.1278),
    ("Paris", "France", 48.8566, 2.3522),
    ("Berlin", "Germany", 52.5200, 13.4050),
    ("Madrid", "Spain", 40.4168, -3.7038),
    ("Rome", "Italy", 41.8933, 12.4829),
    ("Moscow", "Russia", 55.7558, 37.6173),
    ("Istanbul", "Turkey", 41.0082, 28.9784),
    ("Cairo", "Egypt", 30.0444, 31.2357),
    ("Lagos", "Nigeria", 6.4541, 3.3947),
    ("Nairobi", "Kenya", -1.2864, 36.8172),
    ("Johannesburg", "South Africa", -26.2041, 28.0473),
    ("New York", "United States", 40.7128, -74.0060),
    ("Chicago", "United States", 41.8781, -87.6298),
    ("Mexico City", "Mexico", 19.4326, -99.1332),
    ("Bogota", "Colombia", 4.7110, -74.0721),
    ("Sao Paulo", "Brazil", -23.5505, -46.6333),
    ("Buenos Aires", "Argentina", -34.6037, -58.3816),
    ("Delhi", "India", 28.6139, 77.2090),
    ("Dhaka", "Bangladesh", 23.8103, 90.4125),
    ("Bangkok", "Thailand", 13.7563, 100.5018),
    ("Shanghai", "China", 31.2304, 121.4737),
    ("Tokyo", "Japan", 35.6762, 139.6503),
    ("Jakarta", "Indonesia", -6.2088, 106.8456),
    ("Sydney", "Australia", -33.8688, 151.2093),
]

# CMIP6 downscaled GCM models exposed by the Open-Meteo climate API. Verified
# live (June 2026); each contributes a `model` dimension to climate-projections.
CLIMATE_MODELS = ["MRI_AGCM3_2_S", "EC_Earth3P_HR", "MPI_ESM1_2_XR"]
