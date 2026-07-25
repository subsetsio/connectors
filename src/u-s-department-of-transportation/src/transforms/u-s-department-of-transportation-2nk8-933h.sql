-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("terminal_id" AS BIGINT) AS terminal_id,
    CAST("bike_share" AS BIGINT) AS bike_share,
    CAST("terminal_completed" AS BIGINT) AS terminal_completed,
    CAST("in_operation" AS BIGINT) AS in_operation,
    CAST("intercity_bus" AS BIGINT) AS intercity_bus,
    CAST("intercity_rail" AS BIGINT) AS intercity_rail,
    CAST("local_bus" AS BIGINT) AS local_bus,
    CAST("local_rail" AS BIGINT) AS local_rail,
    "terminal_oos_reason",
    "terminal_operated_by",
    "terminal_operation",
    CAST("operator_id" AS BIGINT) AS operator_id,
    CAST("other_access_mode" AS BIGINT) AS other_access_mode,
    "other_access_mode_name",
    "terminal_owned_by",
    "terminal_ownership",
    CAST("parking" AS BIGINT) AS parking,
    CAST("none_access_mode" AS BIGINT) AS none_access_mode,
    CAST("year_added" AS BIGINT) AS year_added,
    CAST("census_year" AS BIGINT) AS census_year,
    CAST("data_year" AS BIGINT) AS data_year
FROM "u-s-department-of-transportation-2nk8-933h"
