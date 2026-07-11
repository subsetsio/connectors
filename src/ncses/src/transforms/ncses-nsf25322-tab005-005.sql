-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Degree field and place of birth" AS degree_field_and_place_of_birth,
    "Total" AS total,
    "S and E occupations" AS s_and_e_occupations,
    "S and E-related occupations" AS s_and_e_related_occupations,
    "Non-S and E occupations" AS non_s_and_e_occupations
FROM "ncses-nsf25322-tab005-005"
