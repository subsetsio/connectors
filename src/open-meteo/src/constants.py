# Curation data for the Open-Meteo connector (data, not logic).
#
# Open-Meteo has no catalog endpoint: data is parameterized by latitude /
# longitude. Each published product table is therefore sampled at a fixed,
# curated set of globally distributed major cities (location is a column, not a
# per-location node). Cities are on or near major rivers so the GloFAS `flood`
# product returns meaningful discharge.
#
# Scope is deliberately bounded to the free non-commercial tier. Open-Meteo
# weights each request as  nLocations * (nDays/14) * (nVariables/10)  and caps
# usage at 10k call-units/day, 5k/hour, 600/min. Bulk multi-decade extraction
# across many cities and variables blows past this by ~20x, so we publish a
# focused 6-city sample with trimmed variable sets and ranges that keeps the
# whole connector's per-run cost (~4.4k units) inside a single hourly bucket.
# (A commercial customer-api key would lift the daily cap and allow far broader
# coverage; the free tier cannot.)

# name, country, latitude, longitude  -- one per inhabited continent, on rivers.
LOCATIONS = [
    ("London", "United Kingdom", 51.5074, -0.1278),   # Thames, Europe
    ("Cairo", "Egypt", 30.0444, 31.2357),             # Nile, Africa
    ("New York", "United States", 40.7128, -74.0060),  # Hudson, N. America
    ("Sao Paulo", "Brazil", -23.5505, -46.6333),      # Tiete, S. America
    ("Tokyo", "Japan", 35.6762, 139.6503),            # Sumida, Asia
    ("Sydney", "Australia", -33.8688, 151.2093),      # Parramatta, Oceania
]

# Single CMIP6 model keeps the (otherwise 100-year-span, very heavy) climate
# product within budget. Verified live (June 2026).
CLIMATE_MODELS = ["MRI_AGCM3_2_S"]
