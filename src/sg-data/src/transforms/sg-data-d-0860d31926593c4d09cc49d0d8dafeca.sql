-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "effective_from",
    "tax_rate"
FROM "sg-data-d-0860d31926593c4d09cc49d0d8dafeca"
