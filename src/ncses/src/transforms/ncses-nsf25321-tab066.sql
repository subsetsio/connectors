-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Occupation" AS occupation,
    "All full-time employed - Median salary" AS all_full_time_employed_median_salary,
    "All full-time employed - SE" AS all_full_time_employed_se,
    "U.S. citizen - Total - Median salary" AS u_s_citizen_total_median_salary,
    "U.S. citizen - Total - SE" AS u_s_citizen_total_se,
    "U.S. citizen - Native born - Median salary" AS u_s_citizen_native_born_median_salary,
    "U.S. citizen - Native born - SE" AS u_s_citizen_native_born_se,
    "U.S. citizen - Naturalized - Median salary" AS u_s_citizen_naturalized_median_salary,
    "U.S. citizen - Naturalized - SE" AS u_s_citizen_naturalized_se,
    "Non-U.S. citizen - Total - Median salary" AS non_u_s_citizen_total_median_salary,
    "Non-U.S. citizen - Total - SE" AS non_u_s_citizen_total_se,
    "Non-U.S. citizen - Permanent resident - Median salary" AS non_u_s_citizen_permanent_resident_median_salary,
    "Non-U.S. citizen - Permanent resident - SE" AS non_u_s_citizen_permanent_resident_se,
    "Non-U.S. citizen - Temporary resident - Median salary" AS non_u_s_citizen_temporary_resident_median_salary,
    "Non-U.S. citizen - Temporary resident - SE" AS non_u_s_citizen_temporary_resident_se
FROM "ncses-nsf25321-tab066"
