-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "birth_year",
    "sex_of_infant",
    "race_or_ethnicity_of_mother",
    "births",
    "percentage"
FROM "nyc-open-data-wffy-3iyg"
