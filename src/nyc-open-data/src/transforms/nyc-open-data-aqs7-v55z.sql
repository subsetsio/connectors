-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "agency_name",
    "name_of_donor_individual_or_firm",
    "type_of_donation",
    "value_of_donation"
FROM "nyc-open-data-aqs7-v55z"
