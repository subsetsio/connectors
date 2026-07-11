-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Characteristic" AS characteristic,
    "All employed - Number" AS all_employed_number,
    "All employed - SE" AS all_employed_se,
    "Science occupations - Total - Number" AS science_occupations_total_number,
    "Science occupations - Total - SE" AS science_occupations_total_se,
    "Science occupations - Biological agricultural and other life scientists - Number" AS science_occupations_biological_agricultural_and_other_life_scientists_number,
    "Science occupations - Biological agricultural and other life scientists - SE" AS science_occupations_biological_agricultural_and_other_life_scientists_se,
    "Science occupations - Computer and information scientists - Number" AS science_occupations_computer_and_information_scientists_number,
    "Science occupations - Computer and information scientists - SE" AS science_occupations_computer_and_information_scientists_se,
    "Science occupations - Mathematical scientists - Number" AS science_occupations_mathematical_scientists_number,
    "Science occupations - Mathematical scientists - SE" AS science_occupations_mathematical_scientists_se,
    "Science occupations - Physical scientists - Number" AS science_occupations_physical_scientists_number,
    "Science occupations - Physical scientists - SE" AS science_occupations_physical_scientists_se,
    "Science occupations - Psychologists - Number" AS science_occupations_psychologists_number,
    "Science occupations - Psychologists - SE" AS science_occupations_psychologists_se,
    "Science occupations - Social scientists - Number" AS science_occupations_social_scientists_number,
    "Science occupations - Social scientists - SE" AS science_occupations_social_scientists_se,
    "Engineering occupations - Social scientists - Number" AS engineering_occupations_social_scientists_number,
    "Engineering occupations - Social scientists - SE" AS engineering_occupations_social_scientists_se,
    "S and E-related occupations - Social scientists - Number" AS s_and_e_related_occupations_social_scientists_number,
    "S and E-related occupations - Social scientists - SE" AS s_and_e_related_occupations_social_scientists_se,
    "Non-S and E occupations - Social scientists - Number" AS non_s_and_e_occupations_social_scientists_number,
    "Non-S and E occupations - Social scientists - SE" AS non_s_and_e_occupations_social_scientists_se
FROM "ncses-nsf25321-tab047"
