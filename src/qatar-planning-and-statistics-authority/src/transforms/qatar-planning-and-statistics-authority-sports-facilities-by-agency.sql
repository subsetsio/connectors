-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "1st_clubs",
    "2nd_clubs",
    "federations",
    "multi_purpose_halls",
    "clubs_total",
    "schools",
    "youth_centers",
    "al_ferjan",
    "other_total",
    "grand_total"
FROM "qatar-planning-and-statistics-authority-sports-facilities-by-agency"
