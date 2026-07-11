-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Fiscal year" AS fiscal_year,
    "Research" AS research,
    "Development - Total" AS development_total,
    "Development - Advanced technology development" AS development_advanced_technology_development,
    "Development - Major systems development" AS development_major_systems_development
FROM "ncses-nsf25339-tab005"
