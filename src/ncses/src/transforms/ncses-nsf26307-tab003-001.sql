-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Broad field" AS broad_field,
    "Total" AS total,
    "Federal - Number" AS federal_number,
    "Federal - Percent" AS federal_percent,
    "Institutional - Number" AS institutional_number,
    "Institutional - Percent" AS institutional_percent,
    "Nonfederal domestic - Number" AS nonfederal_domestic_number,
    "Nonfederal domestic - Percent" AS nonfederal_domestic_percent,
    "Foreign - Number" AS foreign_number,
    "Foreign - Percent" AS foreign_percent,
    "Self-support - Number" AS self_support_number,
    "Self-support - Percent" AS self_support_percent
FROM "ncses-nsf26307-tab003-001"
