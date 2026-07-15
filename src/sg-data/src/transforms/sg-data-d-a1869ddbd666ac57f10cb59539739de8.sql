-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sector",
    "no_of_reg_charities",
    "newly_registered_charities"
FROM "sg-data-d-a1869ddbd666ac57f10cb59539739de8"
