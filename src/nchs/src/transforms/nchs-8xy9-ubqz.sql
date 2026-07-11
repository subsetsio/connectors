-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
SELECT
    "round",
    "indicator",
    "group",
    "subgroup",
    "sample_size",
    "response",
    "percent",
    "standard_error",
    "suppression",
    "significant_1",
    "significant_2"
FROM "nchs-8xy9-ubqz"
