-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: REER and NEER are separate series and should not be summed together.
SELECT
    "series",
    "year",
    "country",
    "value"
FROM "cepii-eqchange"
