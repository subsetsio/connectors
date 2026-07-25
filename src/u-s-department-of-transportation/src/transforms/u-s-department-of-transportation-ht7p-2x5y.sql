-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "state",
    "port",
    CAST("number_of_terminals" AS BIGINT) AS number_of_terminals,
    CAST("on_dock_rail_access" AS BIGINT) AS on_dock_rail_access
FROM "u-s-department-of-transportation-ht7p-2x5y"
