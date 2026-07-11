-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
SELECT
    "round",
    "topic",
    "indicator",
    "title",
    "demographic_variable",
    "demographic_variable_label",
    "percent_estimate",
    "confidence_interval"
FROM "nchs-p89x-xx88"
