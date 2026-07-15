-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "components",
    "tot_tr",
    "trpce"
FROM "sg-data-d-e285a651ec353416054195528ca988a9"
