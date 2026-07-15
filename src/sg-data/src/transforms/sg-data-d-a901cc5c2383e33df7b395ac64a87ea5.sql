-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "artform",
    "operatingreceipts"
FROM "sg-data-d-a901cc5c2383e33df7b395ac64a87ea5"
