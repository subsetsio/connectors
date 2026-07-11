-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Occupation" AS occupation,
    "Labor force participation rate - Percent" AS labor_force_participation_rate_percent,
    "Labor force participation rate - SE" AS labor_force_participation_rate_se
FROM "ncses-nsf25321-tab032-003"
