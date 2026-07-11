-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Level and field of highest degree" AS level_and_field_of_highest_degree,
    "Total" AS total,
    "S and E occupations - Total" AS s_and_e_occupations_total,
    "S and E occupations - Biological agricultural and other life scientists" AS s_and_e_occupations_biological_agricultural_and_other_life_scientists,
    "S and E occupations - Computer and mathematical scientists" AS s_and_e_occupations_computer_and_mathematical_scientists,
    "S and E occupations - Physical and related scientists" AS s_and_e_occupations_physical_and_related_scientists,
    "S and E occupations - Social and related scientists" AS s_and_e_occupations_social_and_related_scientists,
    "S and E occupations - Engineers" AS s_and_e_occupations_engineers,
    "S and E-related occupations - Engineers" AS s_and_e_related_occupations_engineers,
    "Non-S and E occupations - Engineers" AS non_s_and_e_occupations_engineers
FROM "ncses-nsf25322-tab001-002"
