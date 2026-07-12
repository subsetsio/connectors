-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "category",
    "lfy",
    "commodity",
    "lsl",
    "unit_of_measure",
    "whd_lqys",
    "average_price_qr"
FROM "qatar-planning-and-statistics-authority-annual-average-consumer-prices-selected-commodities"
