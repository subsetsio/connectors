-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    CAST("Quarter" AS BIGINT) AS quarter,
    CAST("Month" AS BIGINT) AS month,
    "Pathogen" AS pathogen,
    "Serotype/Species/Subgroup" AS serotype_species_subgroup,
    CAST("Number of isolates" AS BIGINT) AS number_of_isolates,
    CAST("Past two years average" AS DOUBLE) AS past_two_years_average,
    CAST("% Change" AS DOUBLE) AS change
FROM "cdc-ch83-ush6"
