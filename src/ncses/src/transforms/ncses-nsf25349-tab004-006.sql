-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Ethnicity race and debt level - U.S. citizens and permanent residents reporting graduate debt" AS ethnicity_race_and_debt_level_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "All fields - U.S. citizens and permanent residents reporting graduate debt" AS all_fields_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "Science and engineering - Total - U.S. citizens and permanent residents reporting graduate debt" AS science_and_engineering_total_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "Science and engineering - Agricultural sciences and natural resources - U.S. citizens and permanent residents reporting graduate debt" AS science_and_engineering_agricultural_sciences_and_natural_resources_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "Science and engineering - Biological and biomedical sciences - U.S. citizens and permanent residents reporting graduate debt" AS science_and_engineering_biological_and_biomedical_sciences_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "Science and engineering - Computer and information sciences - U.S. citizens and permanent residents reporting graduate debt" AS science_and_engineering_computer_and_information_sciences_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "Science and engineering - Engineering - U.S. citizens and permanent residents reporting graduate debt" AS science_and_engineering_engineering_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "Science and engineering - Geosciences atmospheric and ocean sciences - U.S. citizens and permanent residents reporting graduate debt" AS science_and_engineering_geosciences_atmospheric_and_ocean_sciences_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "Science and engineering - Health sciences - U.S. citizens and permanent residents reporting graduate debt" AS science_and_engineering_health_sciences_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "Science and engineering - Mathematics and statistics - U.S. citizens and permanent residents reporting graduate debt" AS science_and_engineering_mathematics_and_statistics_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "Science and engineering - Multidisciplinary/ interdisciplinary sciences - U.S. citizens and permanent residents reporting graduate debt" AS science_and_engineering_multidisciplinary_interdisciplinary_sciences_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "Science and engineering - Physical sciences - U.S. citizens and permanent residents reporting graduate debt" AS science_and_engineering_physical_sciences_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "Science and engineering - Psychology - U.S. citizens and permanent residents reporting graduate debt" AS science_and_engineering_psychology_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "Science and engineering - Social sciences - U.S. citizens and permanent residents reporting graduate debt" AS science_and_engineering_social_sciences_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "Non-science and engineering - Total - U.S. citizens and permanent residents reporting graduate debt" AS non_science_and_engineering_total_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "Non-science and engineering - Business - U.S. citizens and permanent residents reporting graduate debt" AS non_science_and_engineering_business_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "Non-science and engineering - Education - U.S. citizens and permanent residents reporting graduate debt" AS non_science_and_engineering_education_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "Non-science and engineering - Humanities - U.S. citizens and permanent residents reporting graduate debt" AS non_science_and_engineering_humanities_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "Non-science and engineering - Visual and performing arts - U.S. citizens and permanent residents reporting graduate debt" AS non_science_and_engineering_visual_and_performing_arts_u_s_citizens_and_permanent_residents_reporting_graduate_debt,
    "Non-science and engineering - Other non-science and engineering - U.S. citizens and permanent residents reporting graduate debt" AS non_science_and_engineering_other_non_science_and_engineering_u_s_citizens_and_permanent_residents_reporting_graduate_debt
FROM "ncses-nsf25349-tab004-006"
