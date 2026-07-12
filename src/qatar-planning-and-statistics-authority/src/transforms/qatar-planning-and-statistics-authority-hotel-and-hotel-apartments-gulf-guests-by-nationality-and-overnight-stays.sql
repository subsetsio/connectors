-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "property_type",
    "nw_lmnsh",
    "nationality",
    "ljnsy",
    "metric",
    "lmqys",
    "number"
FROM "qatar-planning-and-statistics-authority-hotel-and-hotel-apartments-gulf-guests-by-nationality-and-overnight-stays"
