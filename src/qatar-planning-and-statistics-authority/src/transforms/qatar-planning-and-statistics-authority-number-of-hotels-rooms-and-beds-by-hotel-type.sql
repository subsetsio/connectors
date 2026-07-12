-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "hotel_class",
    "fy_lfndq",
    "number_of_hotels_dd_lfndq",
    "number_of_rooms_dd_lgrf",
    "number_of_beds_dd_l_sr"
FROM "qatar-planning-and-statistics-authority-number-of-hotels-rooms-and-beds-by-hotel-type"
