-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "qtr",
    "no_of_active_employers"
FROM "sg-data-d-bccb6829056e74f8a87b99c1bdb3e3ab"
