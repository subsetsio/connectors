-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Characteristic" AS characteristic,
    "All employed - Number" AS all_employed_number,
    "All employed - SE" AS all_employed_se,
    "Science - Total - Number" AS science_total_number,
    "Science - Total - SE" AS science_total_se,
    "Science - Biological agricultural and environmental life sciences - Number" AS science_biological_agricultural_and_environmental_life_sciences_number,
    "Science - Biological agricultural and environmental life sciences - SE" AS science_biological_agricultural_and_environmental_life_sciences_se,
    "Science - Computer and information sciences - Number" AS science_computer_and_information_sciences_number,
    "Science - Computer and information sciences - SE" AS science_computer_and_information_sciences_se,
    "Science - Mathematics and statistics - Number" AS science_mathematics_and_statistics_number,
    "Science - Mathematics and statistics - SE" AS science_mathematics_and_statistics_se,
    "Science - Physical sciences - Number" AS science_physical_sciences_number,
    "Science - Physical sciences - SE" AS science_physical_sciences_se,
    "Science - Psychology - Number" AS science_psychology_number,
    "Science - Psychology - SE" AS science_psychology_se,
    "Science - Social sciences - Number" AS science_social_sciences_number,
    "Science - Social sciences - SE" AS science_social_sciences_se,
    "Engineering - Social sciences - Number" AS engineering_social_sciences_number,
    "Engineering - Social sciences - SE" AS engineering_social_sciences_se,
    "Health - Social sciences - Number" AS health_social_sciences_number,
    "Health - Social sciences - SE" AS health_social_sciences_se
FROM "ncses-nsf25321-tab024"
