-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sports_facilities",
    "sports_facilities_ar",
    "federations_clubs_1st_clubs",
    "federations_clubs_2nd_clubs",
    "federations_clubs_federations",
    "federations_clubs_multi_purpose_halls",
    "other_schools",
    "other_youth_centers",
    "other_al_ferjan"
FROM "qatar-planning-and-statistics-authority-sports-facilities-by-type-and-agency-2022"
