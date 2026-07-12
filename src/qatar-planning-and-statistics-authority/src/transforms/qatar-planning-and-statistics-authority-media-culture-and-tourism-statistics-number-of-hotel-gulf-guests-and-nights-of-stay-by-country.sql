-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "country",
    "country_ar",
    "nights_of_stay",
    "number_of_guests"
FROM "qatar-planning-and-statistics-authority-media-culture-and-tourism-statistics-number-of-hotel-gulf-guests-and-nights-of-stay-by-country"
