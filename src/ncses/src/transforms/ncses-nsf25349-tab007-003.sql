-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field and institution" AS field_and_institution,
    "Rank" AS rank,
    "Totala" AS totala,
    "Male" AS male,
    "Female" AS female
FROM "ncses-nsf25349-tab007-003"
