-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Level and field of highest degree" AS level_and_field_of_highest_degree,
    "Total" AS total,
    "Employed - Total" AS employed_total,
    "Employed - S and E occupations" AS employed_s_and_e_occupations,
    "Employed - S and E-related occupations" AS employed_s_and_e_related_occupations,
    "Employed - Non-S and E occupations" AS employed_non_s_and_e_occupations,
    "Unemployeda - Non-S and E occupations" AS unemployeda_non_s_and_e_occupations,
    "Not in labor forceb - Non-S and E occupations" AS not_in_labor_forceb_non_s_and_e_occupations
FROM "ncses-nsf25322-tab001-001"
