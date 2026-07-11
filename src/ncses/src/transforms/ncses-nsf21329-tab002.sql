-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Type of R and D performer and field" AS type_of_r_and_d_performer_and_field,
    "2018",
    "2019",
    "Preliminary - 2020" AS preliminary_2020,
    "Preliminary - % change 2019–20" AS preliminary_change_2019_20
FROM "ncses-nsf21329-tab002"
