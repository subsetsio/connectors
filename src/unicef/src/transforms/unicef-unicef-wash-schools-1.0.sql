-- faithful pass-through of normalized UNICEF SDMX observations.
SELECT
    "ref_area",
    "ref_area_name",
    "indicator",
    "indicator_name",
    "sex",
    "age",
    "time_period",
    "obs_value",
    "unit_measure",
    "obs_status",
    "data_source",
    "lower_bound",
    "upper_bound",
    "dimensions"
FROM "unicef-unicef-wash-schools-1.0"
