-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "years",
    "type_of_vessel_ar",
    "type_of_vessel",
    "month_ar",
    "month",
    "number_tonnage_ar",
    "number_tonnage",
    "value"
FROM "qatar-planning-and-statistics-authority-departing-vessels-gross-and-net-tonnage-by-type-of-vessel-and-month-halul-port"
