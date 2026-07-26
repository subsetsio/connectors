-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "response_id",
    "gispropnum",
    "omppropid",
    "collected_date",
    "time_of_day",
    "_year" AS year,
    "_month" AS month,
    "month_text",
    "_week" AS week,
    "_group" AS group,
    "_location" AS location,
    "ground_syringes",
    "kiosk_syringes",
    "total_syringes",
    "kiosk_number",
    "kiosk_type",
    "precinct",
    "borough",
    "district",
    "property_type",
    "kiosk_site",
    "created_date",
    "_source" AS source
FROM "nyc-open-data-t8xi-d5wb"
