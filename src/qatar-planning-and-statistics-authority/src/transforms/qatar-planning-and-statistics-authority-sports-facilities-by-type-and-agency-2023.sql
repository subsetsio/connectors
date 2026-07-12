-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sports_facility_type",
    "sports_facility_type_ar",
    "1st_clubs",
    "2nd_clubs",
    "federations",
    "multi_purpose_halls",
    "msy_legacy",
    "total_federations_clubs",
    "schools",
    "youth_centers",
    "al_ferjan",
    "total_other",
    "grand_total"
FROM "qatar-planning-and-statistics-authority-sports-facilities-by-type-and-agency-2023"
