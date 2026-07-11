-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Employment sector and occupation" AS employment_sector_and_occupation,
    "All full-time employed - Median salary" AS all_full_time_employed_median_salary,
    "All full-time employed - SE" AS all_full_time_employed_se,
    "Hispanic or Latinoa - Median salary" AS hispanic_or_latinoa_median_salary,
    "Hispanic or Latinoa - SE" AS hispanic_or_latinoa_se,
    "Not Hispanic or Latinob - American Indian or Alaska Native - Median salary" AS not_hispanic_or_latinob_american_indian_or_alaska_native_median_salary,
    "Not Hispanic or Latinob - American Indian or Alaska Native - SE" AS not_hispanic_or_latinob_american_indian_or_alaska_native_se,
    "Not Hispanic or Latinob - Asian - Median salary" AS not_hispanic_or_latinob_asian_median_salary,
    "Not Hispanic or Latinob - Asian - SE" AS not_hispanic_or_latinob_asian_se,
    "Not Hispanic or Latinob - Black or African American - Median salary" AS not_hispanic_or_latinob_black_or_african_american_median_salary,
    "Not Hispanic or Latinob - Black or African American - SE" AS not_hispanic_or_latinob_black_or_african_american_se,
    "Not Hispanic or Latinob - White - Median salary" AS not_hispanic_or_latinob_white_median_salary,
    "Not Hispanic or Latinob - White - SE" AS not_hispanic_or_latinob_white_se,
    "Not Hispanic or Latinob - Other racec - Median salary" AS not_hispanic_or_latinob_other_racec_median_salary,
    "Not Hispanic or Latinob - Other racec - SE" AS not_hispanic_or_latinob_other_racec_se
FROM "ncses-nsf25321-tab072"
