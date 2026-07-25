-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("terminal_id" AS BIGINT) AS terminal_id,
    CAST("operator_id" AS BIGINT) AS operator_id,
    "terminal_name",
    "term_city",
    "term_state",
    "term_country",
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    CAST("in_operation" AS BIGINT) AS in_operation,
    CAST("parking" AS BIGINT) AS parking,
    CAST("local_bus" AS BIGINT) AS local_bus,
    CAST("intercity_bus" AS BIGINT) AS intercity_bus,
    CAST("local_rail" AS BIGINT) AS local_rail,
    CAST("intercity_rail" AS BIGINT) AS intercity_rail,
    CAST("terminal_ownership" AS BIGINT) AS terminal_ownership,
    "terminal_owned_by",
    CAST("terminal_operation" AS BIGINT) AS terminal_operation,
    "terminal_operated_by",
    CAST("census_year" AS BIGINT) AS census_year
FROM "u-s-department-of-transportation-vudg-jaa5"
