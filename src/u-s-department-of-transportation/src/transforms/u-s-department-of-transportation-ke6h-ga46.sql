-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("terminal_id" AS BIGINT) AS terminal_id,
    "term_city",
    CAST("in_operation" AS BOOLEAN) AS in_operation,
    CAST("intercity_bus" AS BOOLEAN) AS intercity_bus,
    CAST("intercity_rail" AS BOOLEAN) AS intercity_rail,
    CAST("local_bus" AS BOOLEAN) AS local_bus,
    CAST("local_rail" AS BOOLEAN) AS local_rail,
    CAST("bike_share" AS BOOLEAN) AS bike_share,
    CAST("parking" AS BOOLEAN) AS parking,
    "terminal_name",
    "terminal_operated_by",
    "terminal_operation",
    CAST("operator_id" AS BIGINT) AS operator_id,
    "terminal_owned_by",
    "terminal_ownership",
    "term_state",
    "term_country",
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    CAST("census_year" AS BIGINT) AS census_year,
    CAST("data_year" AS BIGINT) AS data_year
FROM "u-s-department-of-transportation-ke6h-ga46"
