-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "current_name",
    "states",
    "original_name",
    "current_agency",
    "action",
    "date",
    "year",
    "pres_or_congress",
    "acres_affected"
FROM "fivethirtyeight-antiquities-act-actions-under-antiquities-act"
