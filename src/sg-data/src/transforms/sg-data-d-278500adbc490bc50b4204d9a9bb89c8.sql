-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "education1",
    "reentry_rate_6mth"
FROM "sg-data-d-278500adbc490bc50b4204d9a9bb89c8"
