-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Competition location and event fields describe the competition record; results and scrambles live in separate fact tables.
SELECT
    "id",
    "name",
    "information",
    "external_website",
    "venue",
    "city_name",
    "country_id",
    "venue_address",
    "venue_details",
    "cell_name",
    CAST("cancelled" AS BIGINT) AS cancelled,
    "event_specs",
    "delegates",
    "organizers",
    CAST("year" AS BIGINT) AS year,
    CAST("month" AS BIGINT) AS month,
    CAST("day" AS BIGINT) AS day,
    CAST("end_year" AS BIGINT) AS end_year,
    CAST("end_month" AS BIGINT) AS end_month,
    CAST("end_day" AS BIGINT) AS end_day,
    CAST("latitude_microdegrees" AS BIGINT) AS latitude_microdegrees,
    CAST("longitude_microdegrees" AS BIGINT) AS longitude_microdegrees,
    "_source_table" AS source_table,
    CAST("_export_date" AS TIMESTAMP) AS export_date,
    "_export_version" AS export_version
FROM "wca-competitions"
