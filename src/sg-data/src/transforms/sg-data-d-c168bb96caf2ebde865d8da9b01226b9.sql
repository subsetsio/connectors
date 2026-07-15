-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nature_of_trade_disputes",
    "no._referred" AS no_referred
FROM "sg-data-d-c168bb96caf2ebde865d8da9b01226b9"
