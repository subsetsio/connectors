-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "calendar_week",
    "province_nuts_2_unit_of_deceased",
    "c_5_years_age_group_of_deceased",
    "gender_of_deceased",
    "number_of_deaths"
FROM "statistics-austria-ogd-gest-kalwo-alter-gest-kalwoche-5j-100"
