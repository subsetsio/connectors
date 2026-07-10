-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "table_id",
    "Food_category" AS food_category,
    CAST("Year_first_ill" AS BIGINT) AS year_first_ill,
    "Serotype" AS serotype,
    CAST("No_of_illnesses" AS BIGINT) AS no_of_illnesses,
    CAST("No_of_outbreaks" AS BIGINT) AS no_of_outbreaks,
    "Pathogen" AS pathogen,
    CAST("Year" AS BIGINT) AS year,
    "Year_range" AS year_range,
    CAST("Running_total_by_year_range" AS BIGINT) AS running_total_by_year_range
FROM "cdc-fvm6-ic5r"
