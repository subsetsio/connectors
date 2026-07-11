-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Industry occupation and sex" AS industry_occupation_and_sex,
    "All occupations - All education levels" AS all_occupations_all_education_levels,
    "All occupations - Bachelor's degree or higher" AS all_occupations_bachelor_s_degree_or_higher,
    "All occupations - Less than a bachelor's degree" AS all_occupations_less_than_a_bachelor_s_degree,
    "STEM occupation - All education levels" AS stem_occupation_all_education_levels,
    "STEM occupation - Bachelor's degree or higher" AS stem_occupation_bachelor_s_degree_or_higher,
    "STEM occupation - Less than a bachelor's degree" AS stem_occupation_less_than_a_bachelor_s_degree,
    "Non-STEM occupation - All education levels" AS non_stem_occupation_all_education_levels,
    "Non-STEM occupation - Bachelor's degree or higher" AS non_stem_occupation_bachelor_s_degree_or_higher,
    "Non-STEM occupation - Less than a bachelor's degree" AS non_stem_occupation_less_than_a_bachelor_s_degree
FROM "ncses-nsf25323-tab007"
