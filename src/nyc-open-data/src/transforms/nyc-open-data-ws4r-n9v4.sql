-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "persons_with_hivaids_contact_with_an_animal",
    "persons_with_hivaids_highrisk_sexual_activity_18_years_old",
    "persons_with_hivaids_international_travel",
    "persons_with_hivaids_recreational_water_contact",
    "immunocompetent_persons_contact_with_an_animal",
    "immunocompetent_persons_highrisk_sexual_activity_18_years_old",
    "immunocompetent_persons_international_travel",
    "immunocompetent_persons_recreational_water_contact"
FROM "nyc-open-data-ws4r-n9v4"
