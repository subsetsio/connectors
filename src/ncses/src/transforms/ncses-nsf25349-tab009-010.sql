-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Characteristic" AS characteristic,
    "All multidisciplinary/ interdisciplinary sciences fields" AS all_multidisciplinary_interdisciplinary_sciences_fields,
    "Interdisciplinary computer sciences" AS interdisciplinary_computer_sciences,
    "Multidisciplinary/ interdisciplinary sciences other" AS multidisciplinary_interdisciplinary_sciences_other
FROM "ncses-nsf25349-tab009-010"
