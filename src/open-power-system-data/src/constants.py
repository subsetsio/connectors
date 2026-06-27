"""Entity union for the Open Power System Data connector.

Each id is `<package>__<resource_stem>`, where <package> is the OPSD data-platform
directory slug and <resource_stem> is the CSV filename without extension. The
CSV download URL is derived as:
    https://data.open-power-system-data.org/<package>/latest/<resource_stem>.csv

Copied verbatim from data/sources/open-power-system-data/work/entity_union.json.
"""

ENTITY_IDS = [
    "conventional_power_plants__conventional_power_plants_DE",
    "conventional_power_plants__conventional_power_plants_EU",
    "household_data__household_data_15min_singleindex",
    "household_data__household_data_60min_singleindex",
    "national_generation_capacity__national_generation_capacity_stacked",
    "ninja_pv_wind_profiles__ninja_pv_wind_profiles_singleindex",
    "renewable_power_plants__renewable_capacity_timeseries",
    "renewable_power_plants__renewable_power_plants_CH",
    "renewable_power_plants__renewable_power_plants_CZ",
    "renewable_power_plants__renewable_power_plants_DE",
    "renewable_power_plants__renewable_power_plants_DK",
    "renewable_power_plants__renewable_power_plants_EU",
    "renewable_power_plants__renewable_power_plants_FR",
    "renewable_power_plants__renewable_power_plants_PL",
    "renewable_power_plants__renewable_power_plants_SE",
    "renewable_power_plants__renewable_power_plants_UK",
    "time_series__time_series_15min_singleindex",
    "time_series__time_series_30min_singleindex",
    "time_series__time_series_60min_singleindex",
    "weather_data__weather_data",
    "when2heat__when2heat",
]
