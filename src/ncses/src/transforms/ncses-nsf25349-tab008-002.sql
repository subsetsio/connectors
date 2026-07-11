-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Characteristic" AS characteristic,
    "All fields" AS all_fields,
    "Non-science and engineering - Total" AS non_science_and_engineering_total,
    "Non-science and engineering - Business" AS non_science_and_engineering_business,
    "Non-science and engineering - Education" AS non_science_and_engineering_education,
    "Non-science and engineering - Humanities" AS non_science_and_engineering_humanities,
    "Non-science and engineering - Visual and performing arts" AS non_science_and_engineering_visual_and_performing_arts,
    "Non-science and engineering - Other non-science and engineering" AS non_science_and_engineering_other_non_science_and_engineering
FROM "ncses-nsf25349-tab008-002"
