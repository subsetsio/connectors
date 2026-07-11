-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Onset and duration columns are alternative conflict-onset definitions; select the intended definition before analysis.
SELECT
    "gwno",
    "year",
    "onset2",
    "onset3",
    "onset4",
    "onset5",
    "onset6",
    "onset7",
    "onset8",
    "onset9"
FROM "prio-3"
