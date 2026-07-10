-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "province_nuts_2_unit",
    CAST("year" AS BIGINT) AS year,
    "age_in_single_years",
    "sex",
    "country_of_birth",
    "main_scenario"
FROM "statistics-austria-ogd-bevjahresanfgebland-pr-bevjagb-8"
