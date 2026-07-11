-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an event-level disaster corpus without a stable source row id; multiple rows can share country, year, hazard, and event labels when the source distinguishes records by dates, codes, or displacement figures.
SELECT
    "iso3",
    "country_name",
    "year",
    "start_date",
    "start_date_accuracy",
    "end_date",
    "end_date_accuracy",
    "event_name",
    "new_displacement",
    "new_displacement_rounded",
    "total_displacement",
    "total_displacement_rounded",
    "hazard_category",
    "hazard_category_name",
    "hazard_sub_category",
    "hazard_sub_category_name",
    "hazard_type",
    "hazard_type_name",
    "hazard_sub_type",
    "hazard_sub_type_name",
    "event_codes",
    "event_codes_type"
FROM "idmc-disasters"
