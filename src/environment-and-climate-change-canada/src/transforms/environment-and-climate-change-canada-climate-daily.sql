-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Daily rows are station-day observations; do not aggregate across stations without first choosing the station geography or network intended for the analysis.
SELECT
    "climate_id",
    "station_name",
    "province_code",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "year",
    "month",
    "day",
    "longitude",
    "latitude",
    "data_quality",
    "max_temp",
    "max_temp_flag",
    "min_temp",
    "min_temp_flag",
    "mean_temp",
    "mean_temp_flag",
    "heat_deg_days",
    "heat_deg_days_flag",
    "cool_deg_days",
    "cool_deg_days_flag",
    "total_rain",
    "total_rain_flag",
    "total_snow",
    "total_snow_flag",
    "total_precip",
    "total_precip_flag",
    "snow_on_grnd",
    "snow_on_grnd_flag",
    "dir_of_max_gust",
    "dir_of_max_gust_flag",
    "spd_of_max_gust",
    "spd_of_max_gust_flag"
FROM "environment-and-climate-change-canada-climate-daily"
