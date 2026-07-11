-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Demographic characteristic and field" AS demographic_characteristic_and_field,
    "Total number" AS total_number,
    "Highest level of parental education % - All" AS highest_level_of_parental_education_all,
    "Highest level of parental education % - High school or less" AS highest_level_of_parental_education_high_school_or_less,
    "Highest level of parental education % - Some collegea" AS highest_level_of_parental_education_some_collegea,
    "Highest level of parental education % - Bachelor's degree" AS highest_level_of_parental_education_bachelor_s_degree,
    "Highest level of parental education % - Master's degree" AS highest_level_of_parental_education_master_s_degree,
    "Highest level of parental education % - Professional doctorateb" AS highest_level_of_parental_education_professional_doctorateb,
    "Highest level of parental education % - Research doctorate" AS highest_level_of_parental_education_research_doctorate
FROM "ncses-nsf25349-tab005-005"
