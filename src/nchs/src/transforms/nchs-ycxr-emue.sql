-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
SELECT
    "year",
    "measure_type",
    "leading_10_ranking",
    "measure",
    "group",
    "subgroup",
    "estimate_type",
    "estimate",
    "standard_error",
    "lower_95_ci",
    "upper_95_ci",
    "reliable"
FROM "nchs-ycxr-emue"
