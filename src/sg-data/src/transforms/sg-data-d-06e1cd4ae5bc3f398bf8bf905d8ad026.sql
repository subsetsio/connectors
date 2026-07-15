-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SAF_Service" AS saf_service,
    "Career_scheme" AS career_scheme,
    "Vocation" AS vocation,
    "Link" AS link,
    "Responsibilities" AS responsibilities,
    "Eligibility_and_academic_qualifications" AS eligibility_and_academic_qualifications,
    "Benefits" AS benefits
FROM "sg-data-d-06e1cd4ae5bc3f398bf8bf905d8ad026"
