-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Time to degree and demographic characteristic - Years since bachelor's degree" AS time_to_degree_and_demographic_characteristic_years_since_bachelor_s_degree,
    "All fields - Number - Years since bachelor's degree" AS all_fields_number_years_since_bachelor_s_degree,
    "All fields - Median - Years since bachelor's degree" AS all_fields_median_years_since_bachelor_s_degree,
    "Non-science and engineering total - Number - Years since bachelor's degree" AS non_science_and_engineering_total_number_years_since_bachelor_s_degree,
    "Non-science and engineering total - Median - Years since bachelor's degree" AS non_science_and_engineering_total_median_years_since_bachelor_s_degree,
    "Business - Number - Years since bachelor's degree" AS business_number_years_since_bachelor_s_degree,
    "Business - Median - Years since bachelor's degree" AS business_median_years_since_bachelor_s_degree,
    "Education - Number - Years since bachelor's degree" AS education_number_years_since_bachelor_s_degree,
    "Education - Median - Years since bachelor's degree" AS education_median_years_since_bachelor_s_degree,
    "Humanities - Number - Years since bachelor's degree" AS humanities_number_years_since_bachelor_s_degree,
    "Humanities - Median - Years since bachelor's degree" AS humanities_median_years_since_bachelor_s_degree,
    "Visual and performing arts - Number - Years since bachelor's degree" AS visual_and_performing_arts_number_years_since_bachelor_s_degree,
    "Visual and performing arts - Median - Years since bachelor's degree" AS visual_and_performing_arts_median_years_since_bachelor_s_degree,
    "Other non-science and engineering - Number - Years since bachelor's degree" AS other_non_science_and_engineering_number_years_since_bachelor_s_degree,
    "Other non-science and engineering - Median - Years since bachelor's degree" AS other_non_science_and_engineering_median_years_since_bachelor_s_degree
FROM "ncses-nsf25349-tab003-006"
