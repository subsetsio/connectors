-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The category column is a broad occupation group, not geography; compare ratios across categories rather than summing them.
SELECT
    "date",
    CAST("period_label" AS BIGINT) AS period_label,
    "category",
    "measure",
    "value"
FROM "nationwide-hpi-ftb-hper-by-broad-occupation"
