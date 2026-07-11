-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Field of study" AS field_of_study,
    "Total - Number" AS total_number,
    "Total - SE" AS total_se,
    "Hispanic or Latinoa - Number" AS hispanic_or_latinoa_number,
    "Hispanic or Latinoa - SE" AS hispanic_or_latinoa_se,
    "Not Hispanic or Latinob - American Indian or Alaska Native - Number" AS not_hispanic_or_latinob_american_indian_or_alaska_native_number,
    "Not Hispanic or Latinob - American Indian or Alaska Native - SE" AS not_hispanic_or_latinob_american_indian_or_alaska_native_se,
    "Not Hispanic or Latinob - Asian - Number" AS not_hispanic_or_latinob_asian_number,
    "Not Hispanic or Latinob - Asian - SE" AS not_hispanic_or_latinob_asian_se,
    "Not Hispanic or Latinob - Black or African American - Number" AS not_hispanic_or_latinob_black_or_african_american_number,
    "Not Hispanic or Latinob - Black or African American - SE" AS not_hispanic_or_latinob_black_or_african_american_se,
    "Not Hispanic or Latinob - White - Number" AS not_hispanic_or_latinob_white_number,
    "Not Hispanic or Latinob - White - SE" AS not_hispanic_or_latinob_white_se,
    "Not Hispanic or Latinob - Other racec - Number" AS not_hispanic_or_latinob_other_racec_number,
    "Not Hispanic or Latinob - Other racec - SE" AS not_hispanic_or_latinob_other_racec_se
FROM "ncses-nsf25321-tab006"
