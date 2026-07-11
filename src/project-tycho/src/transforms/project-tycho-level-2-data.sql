-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source includes both state and city location rows; filter loc_type before geographic aggregation.
-- caution: Rows mix CASES and DEATHS event types; filter event before aggregating counts.
-- caution: The raw table contains a small number of exact duplicate observation rows, so aggregate with care.
SELECT
    CAST("epi_week" AS BIGINT) AS epi_week,
    "country",
    "state",
    "loc",
    "loc_type",
    "disease",
    "event",
    CAST("number" AS BIGINT) AS number,
    strptime("from_date", '%Y-%m-%d')::DATE AS from_date,
    strptime("to_date", '%Y-%m-%d')::DATE AS to_date,
    "url"
FROM "project-tycho-level-2-data"
