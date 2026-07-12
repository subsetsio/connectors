-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "educational_attainment_of_woman_mother",
    "de_facto_marital_status_of_woman_mother",
    "ethnic_nationality_of_woman_mother",
    "age_of_woman_mother",
    "legal_marital_status_of_woman_mother",
    "economic_activity_of_woman_mother",
    "place_of_residence_of_woman_mother",
    "value"
FROM "statistics-estonia-rl212.px"
