-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "public_youth_centers",
    "specialized_youth_centers",
    "youth_centers_for_people_with_disabilities",
    "clubs_and_associations_of_youth_hobbies"
FROM "qatar-planning-and-statistics-authority-youth-and-sports-institutions-by-type"
