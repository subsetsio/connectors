-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Vaccine/Exemption" AS vaccine_exemption,
    "Dose" AS dose,
    "Geography Type" AS geography_type,
    "Geography" AS geography,
    "School Year" AS school_year,
    "Estimate (%)" AS estimate,
    CAST("Population Size" AS BIGINT) AS population_size,
    CAST("Percent Surveyed" AS DOUBLE) AS percent_surveyed,
    "Footnotes" AS footnotes,
    CAST("Number of Exemptions" AS BIGINT) AS number_of_exemptions,
    "Survey Type" AS survey_type
FROM "cdc-ijqb-a7ye"
