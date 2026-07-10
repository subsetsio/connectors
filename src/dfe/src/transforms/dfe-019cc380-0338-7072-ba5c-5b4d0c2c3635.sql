-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "geographic_level",
    "country_code",
    "country_name",
    "total_neet_net",
    "health_condition_grouping",
    "health_condition",
    CAST("population_count" AS DOUBLE) AS population_count,
    CAST("sample_size_count" AS BIGINT) AS sample_size_count,
    "population_count_ci_plusminus",
    "population_count_lower",
    "population_count_upper",
    "population_percent",
    "population_percent_ci_plusminus",
    "population_percent_lower",
    "population_percent_upper",
    "percent_of_neet"
FROM "dfe-019cc380-0338-7072-ba5c-5b4d0c2c3635"
