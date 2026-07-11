-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Level and field of highest degree" AS level_and_field_of_highest_degree,
    "All - Total" AS all_total,
    "All - Closely related" AS all_closely_related,
    "All - Somewhat related" AS all_somewhat_related,
    "All - Not related" AS all_not_related,
    "S and E occupations - Total" AS s_and_e_occupations_total,
    "S and E occupations - Closely related" AS s_and_e_occupations_closely_related,
    "S and E occupations - Somewhat related" AS s_and_e_occupations_somewhat_related,
    "S and E occupations - Not related" AS s_and_e_occupations_not_related,
    "S and E-related occupations - Total" AS s_and_e_related_occupations_total,
    "S and E-related occupations - Closely related" AS s_and_e_related_occupations_closely_related,
    "S and E-related occupations - Somewhat related" AS s_and_e_related_occupations_somewhat_related,
    "S and E-related occupations - Not related" AS s_and_e_related_occupations_not_related,
    "Non-S and E occupations - Total" AS non_s_and_e_occupations_total,
    "Non-S and E occupations - Closely related" AS non_s_and_e_occupations_closely_related,
    "Non-S and E occupations - Somewhat related" AS non_s_and_e_occupations_somewhat_related,
    "Non-S and E occupations - Not related" AS non_s_and_e_occupations_not_related
FROM "ncses-nsf25322-tab001-003"
