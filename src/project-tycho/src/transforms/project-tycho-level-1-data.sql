-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source includes both state and city location rows; filter loc_type before geographic aggregation.
-- caution: The raw table contains a small number of exact duplicate observation rows, so aggregate with care.
SELECT
    CAST("epi_week" AS BIGINT) AS epi_week,
    "state",
    "loc",
    "loc_type",
    "disease",
    "cases",
    CAST("incidence_per_100000" AS DOUBLE) AS incidence_per_100000
FROM "project-tycho-level-1-data"
