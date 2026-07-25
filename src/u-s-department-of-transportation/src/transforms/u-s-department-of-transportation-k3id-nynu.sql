-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "a_weighted_24_hour_laeq_dba",
    CAST("population_exposed" AS BIGINT) AS population_exposed,
    CAST("percent_of_total_population" AS DOUBLE) AS percent_of_total_population
FROM "u-s-department-of-transportation-k3id-nynu"
