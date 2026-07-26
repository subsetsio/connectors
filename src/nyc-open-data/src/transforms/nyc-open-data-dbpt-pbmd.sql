-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "func_code",
    "function_description",
    "employment_status",
    "job_category",
    "line_no",
    "salary_band",
    "hispaniclatino_male",
    "hispancilatino_female",
    "non_hispaniclatino_male_white",
    "nonhispaniclatino_male_black",
    "nonhispaniclatino_male_asian",
    "nonhispaniclatino_male_nhopi",
    "nonhispaniclatino_male_amer_ind",
    "nonhispaniclatino_male_2_races",
    "non_hispaniclatino_female_white",
    "nonhispaniclatino_female_black",
    "nonhispaniclatino_female_asian",
    "nonhispaniclatino_female_nhopi",
    "nonhispaniclatino_female_amer_ind",
    "nonhispaniclatino_female_2_races",
    "total",
    "fy"
FROM "nyc-open-data-dbpt-pbmd"
