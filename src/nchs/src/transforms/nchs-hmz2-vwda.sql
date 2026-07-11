-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "state",
    "year",
    "month",
    "period",
    "indicator",
    "data_value"
FROM "nchs-hmz2-vwda"
