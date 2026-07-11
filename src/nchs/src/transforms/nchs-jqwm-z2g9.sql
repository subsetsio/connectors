-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_and_quarter",
    "topic",
    "indicator",
    "time_period",
    "rate",
    "unit",
    "significant",
    "standard_error",
    "footnote_symbol",
    "footnote"
FROM "nchs-jqwm-z2g9"
