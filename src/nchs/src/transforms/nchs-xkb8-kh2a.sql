-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
SELECT
    "state",
    "year",
    "month",
    "period",
    "indicator",
    "data_value",
    "percent_complete",
    "percent_pending_investigation",
    "state_name",
    "footnote",
    "footnote_symbol",
    "predicted_value"
FROM "nchs-xkb8-kh2a"
