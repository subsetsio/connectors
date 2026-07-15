-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nitrogen_dioxide_mean"
FROM "sg-data-d-88dcbdd26f7adbb5a469491378abfedc"
