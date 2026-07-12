-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "ljnsy",
    "hotel_rating",
    "drj_lfndq",
    "metric",
    "lmqys",
    "number"
FROM "qatar-planning-and-statistics-authority-hotel-guests-by-nationality-hotel-rating-and-hotel-stays"
