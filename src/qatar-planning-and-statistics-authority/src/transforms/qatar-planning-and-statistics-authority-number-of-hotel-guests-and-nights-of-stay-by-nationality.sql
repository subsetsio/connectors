-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "arab_nationalities_guests",
    "arab_nationalities_nights",
    "foreign_nationalities_guest",
    "foreign_nationalities_nights"
FROM "qatar-planning-and-statistics-authority-number-of-hotel-guests-and-nights-of-stay-by-nationality"
