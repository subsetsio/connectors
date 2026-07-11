-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Characteristic" AS characteristic,
    "All other non-science and engineering fields" AS all_other_non_science_and_engineering_fields,
    "Communication and journalism" AS communication_and_journalism,
    "Multidisciplinary/ interdisciplinary studies" AS multidisciplinary_interdisciplinary_studies,
    "Public administration and social services" AS public_administration_and_social_services,
    "Non-science and engineering other" AS non_science_and_engineering_other
FROM "ncses-nsf25349-tab008-018"
