-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "person",
    "dept",
    "eow",
    "cause",
    "cause_short",
    "date",
    "year",
    "canine",
    "dept_name",
    "state"
FROM "fivethirtyeight-police-deaths-clean-data"
