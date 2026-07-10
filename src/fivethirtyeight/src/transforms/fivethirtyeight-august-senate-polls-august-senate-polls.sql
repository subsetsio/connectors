-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cycle",
    "state",
    "senate_class",
    "start_date",
    "end_date",
    "DEM_poll" AS dem_poll,
    "REP_poll" AS rep_poll,
    "DEM_result" AS dem_result,
    "REP_result" AS rep_result,
    "error",
    "absolute_error"
FROM "fivethirtyeight-august-senate-polls-august-senate-polls"
