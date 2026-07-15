-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry",
    "occupation",
    "recruitment_rate"
FROM "sg-data-d-505835a6bca594ee8ba8a7e72a646f2f"
