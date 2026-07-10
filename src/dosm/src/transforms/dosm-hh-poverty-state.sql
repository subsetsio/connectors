-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "state",
    "date",
    "poverty_absolute",
    "poverty_hardcore",
    "poverty_relative"
FROM "dosm-hh-poverty-state"
