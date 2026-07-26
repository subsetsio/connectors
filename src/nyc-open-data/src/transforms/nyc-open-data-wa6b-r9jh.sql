-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "survey_year",
    "id",
    "district",
    "survey_language",
    "information",
    "gender",
    "ethnicity",
    "ethnicity_other",
    "education",
    "income",
    "preferred_language",
    "preferred_language_other",
    "age",
    "ballot",
    "voted_recently"
FROM "nyc-open-data-wa6b-r9jh"
