-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Time to degree and demographic characteristic - Years since bachelor's degree" AS time_to_degree_and_demographic_characteristic_years_since_bachelor_s_degree,
    "All fields - Number - Years since bachelor's degree" AS all_fields_number_years_since_bachelor_s_degree,
    "All fields - Median - Years since bachelor's degree" AS all_fields_median_years_since_bachelor_s_degree,
    "Science and engineering total - Number - Years since bachelor's degree" AS science_and_engineering_total_number_years_since_bachelor_s_degree,
    "Science and engineering total - Median - Years since bachelor's degree" AS science_and_engineering_total_median_years_since_bachelor_s_degree,
    "Agricultural sciences and natural resources - Number - Years since bachelor's degree" AS agricultural_sciences_and_natural_resources_number_years_since_bachelor_s_degree,
    "Agricultural sciences and natural resources - Median - Years since bachelor's degree" AS agricultural_sciences_and_natural_resources_median_years_since_bachelor_s_degree,
    "Biological and biomedical sciences - Number - Years since bachelor's degree" AS biological_and_biomedical_sciences_number_years_since_bachelor_s_degree,
    "Biological and biomedical sciences - Median - Years since bachelor's degree" AS biological_and_biomedical_sciences_median_years_since_bachelor_s_degree,
    "Computer and information sciences - Number - Years since bachelor's degree" AS computer_and_information_sciences_number_years_since_bachelor_s_degree,
    "Computer and information sciences - Median - Years since bachelor's degree" AS computer_and_information_sciences_median_years_since_bachelor_s_degree,
    "Engineering - Number - Years since bachelor's degree" AS engineering_number_years_since_bachelor_s_degree,
    "Engineering - Median - Years since bachelor's degree" AS engineering_median_years_since_bachelor_s_degree,
    "Geosciences atmospheric and ocean sciences - Number - Years since bachelor's degree" AS geosciences_atmospheric_and_ocean_sciences_number_years_since_bachelor_s_degree,
    "Geosciences atmospheric and ocean sciences - Median - Years since bachelor's degree" AS geosciences_atmospheric_and_ocean_sciences_median_years_since_bachelor_s_degree,
    "Health sciences - Number - Years since bachelor's degree" AS health_sciences_number_years_since_bachelor_s_degree,
    "Health sciences - Median - Years since bachelor's degree" AS health_sciences_median_years_since_bachelor_s_degree,
    "Mathematics and statistics - Number - Years since bachelor's degree" AS mathematics_and_statistics_number_years_since_bachelor_s_degree,
    "Mathematics and statistics - Median - Years since bachelor's degree" AS mathematics_and_statistics_median_years_since_bachelor_s_degree,
    "Multidisciplinary/ interdisciplinary sciences - Number - Years since bachelor's degree" AS multidisciplinary_interdisciplinary_sciences_number_years_since_bachelor_s_degree,
    "Multidisciplinary/ interdisciplinary sciences - Median - Years since bachelor's degree" AS multidisciplinary_interdisciplinary_sciences_median_years_since_bachelor_s_degree,
    "Physical sciences - Number - Years since bachelor's degree" AS physical_sciences_number_years_since_bachelor_s_degree,
    "Physical sciences - Median - Years since bachelor's degree" AS physical_sciences_median_years_since_bachelor_s_degree,
    "Psychology - Number - Years since bachelor's degree" AS psychology_number_years_since_bachelor_s_degree,
    "Psychology - Median - Years since bachelor's degree" AS psychology_median_years_since_bachelor_s_degree,
    "Social sciences - Number - Years since bachelor's degree" AS social_sciences_number_years_since_bachelor_s_degree,
    "Social sciences - Median - Years since bachelor's degree" AS social_sciences_median_years_since_bachelor_s_degree
FROM "ncses-nsf25349-tab003-005"
