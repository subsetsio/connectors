-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry1",
    "industry2",
    "industry3",
    "work_week_pattern",
    "distribution"
FROM "sg-data-d-8787647de610dbaafb1e9cfb830a9363"
