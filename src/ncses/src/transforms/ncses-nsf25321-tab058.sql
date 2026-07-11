-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Employer location" AS employer_location,
    "All fields - Median salary" AS all_fields_median_salary,
    "All fields - SE" AS all_fields_se,
    "Science - Total - Median salary" AS science_total_median_salary,
    "Science - Total - SE" AS science_total_se,
    "Science - Biological agricultural and environmental life sciences - Median salary" AS science_biological_agricultural_and_environmental_life_sciences_median_salary,
    "Science - Biological agricultural and environmental life sciences - SE" AS science_biological_agricultural_and_environmental_life_sciences_se,
    "Science - Computer and information sciences - Median salary" AS science_computer_and_information_sciences_median_salary,
    "Science - Computer and information sciences - SE" AS science_computer_and_information_sciences_se,
    "Science - Mathematics and statistics - Median salary" AS science_mathematics_and_statistics_median_salary,
    "Science - Mathematics and statistics - SE" AS science_mathematics_and_statistics_se,
    "Science - Physical sciences - Median salary" AS science_physical_sciences_median_salary,
    "Science - Physical sciences - SE" AS science_physical_sciences_se,
    "Science - Psychology - Median salary" AS science_psychology_median_salary,
    "Science - Psychology - SE" AS science_psychology_se,
    "Science - Social sciences - Median salary" AS science_social_sciences_median_salary,
    "Science - Social sciences - SE" AS science_social_sciences_se,
    "Engineering - Social sciences - Median salary" AS engineering_social_sciences_median_salary,
    "Engineering - Social sciences - SE" AS engineering_social_sciences_se,
    "Health - Social sciences - Median salary" AS health_social_sciences_median_salary,
    "Health - Social sciences - SE" AS health_social_sciences_se
FROM "ncses-nsf25321-tab058"
