-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("terminal_id" AS BIGINT) AS terminal_id,
    "terminal_name",
    "term_city",
    "term_state",
    "term_country",
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    CAST("in_operation" AS BIGINT) AS in_operation,
    CAST("intercity_bus" AS BIGINT) AS intercity_bus,
    CAST("intercity_rail" AS BIGINT) AS intercity_rail,
    CAST("local_bus" AS BIGINT) AS local_bus,
    CAST("local_rail" AS BIGINT) AS local_rail,
    CAST("bike_share" AS BIGINT) AS bike_share,
    CAST("parking" AS BIGINT) AS parking,
    "terminal_operation",
    "terminal_ownership",
    CAST("number_of_operators" AS BIGINT) AS number_of_operators,
    CAST("census_year" AS BIGINT) AS census_year
FROM "u-s-department-of-transportation-difu-6bgs"
