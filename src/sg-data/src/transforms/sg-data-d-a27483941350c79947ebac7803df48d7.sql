-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "level",
    "course",
    "sex",
    "enrolment_preu"
FROM "sg-data-d-a27483941350c79947ebac7803df48d7"
