-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
SELECT
    "figure",
    "setting",
    "indicator",
    "group",
    "subgroup",
    "time",
    strptime("start_time", '%m/%d/%Y')::DATE AS start_time,
    strptime("end_time", '%m/%d/%Y')::DATE AS end_time,
    "value",
    "measure"
FROM "nchs-q3t8-zr7t"
