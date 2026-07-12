-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "educational_attainment_of_woman",
    "de_facto_marital_status_of_woman",
    "age_group_of_woman",
    "legal_marital_status_of_woman",
    "ethnic_nationality_of_woman",
    "place_of_residence_of_woman",
    "indicator",
    "value"
FROM "statistics-estonia-rl0415.px"
