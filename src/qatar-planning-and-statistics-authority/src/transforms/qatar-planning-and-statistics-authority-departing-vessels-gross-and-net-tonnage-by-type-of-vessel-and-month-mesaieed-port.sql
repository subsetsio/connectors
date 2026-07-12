-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "years",
    "nw_lsfyn",
    "type_of_vessel",
    "lshhr",
    "month",
    "dd_lsfn_w_lhmwl",
    "number_tonnage",
    "value"
FROM "qatar-planning-and-statistics-authority-departing-vessels-gross-and-net-tonnage-by-type-of-vessel-and-month-mesaieed-port"
