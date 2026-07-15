-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "industry",
    "occupation",
    "recruitment_rate"
FROM "sg-data-d-785903005a276ca9efdeab97707cdbbf"
