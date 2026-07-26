-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "income_group",
    "total_nyc_pit_liability",
    "avg_pit_liability",
    "number_of_tax_payers"
FROM "nyc-open-data-3vvi-fwjs"
