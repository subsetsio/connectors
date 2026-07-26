-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "raceethnicity",
    "age_group_1_year_number_rate",
    "age_group_14_years_number_rate",
    "age_group_5_years_number_rate",
    "age_group_59_years_number_rate",
    "age_group_1019_years_number_rate",
    "age_group_2044_years_number_rate",
    "age_group_4559_years_number_rate",
    "age_group_60_years_number_rate",
    "citywide_number_rate",
    "manhattan_number_rate",
    "bronx_number_rate",
    "brooklyn_number_rate",
    "queens_number_rate",
    "staten_island_number_rate"
FROM "nyc-open-data-fkec-mjr6"
