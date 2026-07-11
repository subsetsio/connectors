-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Employer location" AS employer_location,
    "All full-time employed - Median salary" AS all_full_time_employed_median_salary,
    "All full-time employed - SE" AS all_full_time_employed_se,
    "Science occupations - Total - Median salary" AS science_occupations_total_median_salary,
    "Science occupations - Total - SE" AS science_occupations_total_se,
    "Science occupations - Biological agricultural and other life scientists - Median salary" AS science_occupations_biological_agricultural_and_other_life_scientists_median_salary,
    "Science occupations - Biological agricultural and other life scientists - SE" AS science_occupations_biological_agricultural_and_other_life_scientists_se,
    "Science occupations - Computer and information scientists - Median salary" AS science_occupations_computer_and_information_scientists_median_salary,
    "Science occupations - Computer and information scientists - SE" AS science_occupations_computer_and_information_scientists_se,
    "Science occupations - Mathematical scientists - Median salary" AS science_occupations_mathematical_scientists_median_salary,
    "Science occupations - Mathematical scientists - SE" AS science_occupations_mathematical_scientists_se,
    "Science occupations - Physical scientists - Median salary" AS science_occupations_physical_scientists_median_salary,
    "Science occupations - Physical scientists - SE" AS science_occupations_physical_scientists_se,
    "Science occupations - Psychologists - Median salary" AS science_occupations_psychologists_median_salary,
    "Science occupations - Psychologists - SE" AS science_occupations_psychologists_se,
    "Science occupations - Social scientists - Median salary" AS science_occupations_social_scientists_median_salary,
    "Science occupations - Social scientists - SE" AS science_occupations_social_scientists_se,
    "Engineering occupations - Social scientists - Median salary" AS engineering_occupations_social_scientists_median_salary,
    "Engineering occupations - Social scientists - SE" AS engineering_occupations_social_scientists_se,
    "S and E-related occupations - Social scientists - Median salary" AS s_and_e_related_occupations_social_scientists_median_salary,
    "S and E-related occupations - Social scientists - SE" AS s_and_e_related_occupations_social_scientists_se,
    "Non-S and E occupations - Social scientists - Median salary" AS non_s_and_e_occupations_social_scientists_median_salary,
    "Non-S and E occupations - Social scientists - SE" AS non_s_and_e_occupations_social_scientists_se
FROM "ncses-nsf25321-tab074"
