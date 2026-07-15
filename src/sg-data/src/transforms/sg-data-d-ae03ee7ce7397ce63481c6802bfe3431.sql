-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry",
    "retrench_term_contract"
FROM "sg-data-d-ae03ee7ce7397ce63481c6802bfe3431"
