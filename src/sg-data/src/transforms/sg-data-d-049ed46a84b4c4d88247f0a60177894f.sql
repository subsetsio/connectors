-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "admissions_by_age_group",
    "number_of_admission"
FROM "sg-data-d-049ed46a84b4c4d88247f0a60177894f"
