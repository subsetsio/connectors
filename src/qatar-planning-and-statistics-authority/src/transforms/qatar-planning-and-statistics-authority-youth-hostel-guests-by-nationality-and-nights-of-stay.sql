-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nationality",
    "nationality_ar",
    "2019_guests",
    "2019_nights_of_stay",
    "2020_guests",
    "2020_nights_of_stay",
    "2021_guests",
    "2021_nights_of_stay",
    "2022_guests",
    "2022_nights_of_stay",
    "2023_guests",
    "2023_nights_of_stay"
FROM "qatar-planning-and-statistics-authority-youth-hostel-guests-by-nationality-and-nights-of-stay"
