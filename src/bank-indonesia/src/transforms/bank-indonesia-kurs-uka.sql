-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rates are for physical foreign banknotes and can differ from BI transaction rates because the product and spread are different.
-- caution: Rates are quoted against IDR with the source's unit field; consumers should account for unit before comparing currency levels.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "currency",
    "unit",
    "buy",
    "sell"
FROM "bank-indonesia-kurs-uka"
