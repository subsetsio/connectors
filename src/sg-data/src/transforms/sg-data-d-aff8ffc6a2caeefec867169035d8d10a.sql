-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nature_of_trade_disputes",
    "no._awarded" AS no_awarded
FROM "sg-data-d-aff8ffc6a2caeefec867169035d8d10a"
