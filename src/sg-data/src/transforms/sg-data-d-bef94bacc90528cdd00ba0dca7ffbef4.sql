-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "qtr",
    "cost_of_current_holdings"
FROM "sg-data-d-bef94bacc90528cdd00ba0dca7ffbef4"
