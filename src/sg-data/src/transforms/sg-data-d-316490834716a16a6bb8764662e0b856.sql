-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bo_date",
    "bankruptcy_no"
FROM "sg-data-d-316490834716a16a6bb8764662e0b856"
