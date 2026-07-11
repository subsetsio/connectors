-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Occupation" AS occupation,
    "All employed minoritya - Total - Number" AS all_employed_minoritya_total_number,
    "All employed minoritya - Total - SE" AS all_employed_minoritya_total_se,
    "All employed minoritya - Male - Number" AS all_employed_minoritya_male_number,
    "All employed minoritya - Male - SE" AS all_employed_minoritya_male_se,
    "All employed minoritya - Female - Number" AS all_employed_minoritya_female_number,
    "All employed minoritya - Female - SE" AS all_employed_minoritya_female_se,
    "Hispanic or Latinob - Total - Number" AS hispanic_or_latinob_total_number,
    "Hispanic or Latinob - Total - SE" AS hispanic_or_latinob_total_se,
    "Hispanic or Latinob - Male - Number" AS hispanic_or_latinob_male_number,
    "Hispanic or Latinob - Male - SE" AS hispanic_or_latinob_male_se,
    "Hispanic or Latinob - Female - Number" AS hispanic_or_latinob_female_number,
    "Hispanic or Latinob - Female - SE" AS hispanic_or_latinob_female_se,
    "Not Hispanic or Latinoc - American Indian or Alaska Native - Total - Number" AS not_hispanic_or_latinoc_american_indian_or_alaska_native_total_number,
    "Not Hispanic or Latinoc - American Indian or Alaska Native - Total - SE" AS not_hispanic_or_latinoc_american_indian_or_alaska_native_total_se,
    "Not Hispanic or Latinoc - American Indian or Alaska Native - Male - Number" AS not_hispanic_or_latinoc_american_indian_or_alaska_native_male_number,
    "Not Hispanic or Latinoc - American Indian or Alaska Native - Male - SE" AS not_hispanic_or_latinoc_american_indian_or_alaska_native_male_se,
    "Not Hispanic or Latinoc - American Indian or Alaska Native - Female - Number" AS not_hispanic_or_latinoc_american_indian_or_alaska_native_female_number,
    "Not Hispanic or Latinoc - American Indian or Alaska Native - Female - SE" AS not_hispanic_or_latinoc_american_indian_or_alaska_native_female_se,
    "Not Hispanic or Latinoc - Black or African American - Total - Number" AS not_hispanic_or_latinoc_black_or_african_american_total_number,
    "Not Hispanic or Latinoc - Black or African American - Total - SE" AS not_hispanic_or_latinoc_black_or_african_american_total_se,
    "Not Hispanic or Latinoc - Black or African American - Male - Number" AS not_hispanic_or_latinoc_black_or_african_american_male_number,
    "Not Hispanic or Latinoc - Black or African American - Male - SE" AS not_hispanic_or_latinoc_black_or_african_american_male_se,
    "Not Hispanic or Latinoc - Black or African American - Female - Number" AS not_hispanic_or_latinoc_black_or_african_american_female_number,
    "Not Hispanic or Latinoc - Black or African American - Female - SE" AS not_hispanic_or_latinoc_black_or_african_american_female_se,
    "Not Hispanic or Latinoc - Native Hawaiian or Other Pacific Islander - Total - Number" AS not_hispanic_or_latinoc_native_hawaiian_or_other_pacific_islander_total_number,
    "Not Hispanic or Latinoc - Native Hawaiian or Other Pacific Islander - Total - SE" AS not_hispanic_or_latinoc_native_hawaiian_or_other_pacific_islander_total_se,
    "Not Hispanic or Latinoc - Native Hawaiian or Other Pacific Islander - Male - Number" AS not_hispanic_or_latinoc_native_hawaiian_or_other_pacific_islander_male_number,
    "Not Hispanic or Latinoc - Native Hawaiian or Other Pacific Islander - Male - SE" AS not_hispanic_or_latinoc_native_hawaiian_or_other_pacific_islander_male_se,
    "Not Hispanic or Latinoc - Native Hawaiian or Other Pacific Islander - Female - Number" AS not_hispanic_or_latinoc_native_hawaiian_or_other_pacific_islander_female_number,
    "Not Hispanic or Latinoc - Native Hawaiian or Other Pacific Islander - Female - SE" AS not_hispanic_or_latinoc_native_hawaiian_or_other_pacific_islander_female_se
FROM "ncses-nsf25321-tab038"
