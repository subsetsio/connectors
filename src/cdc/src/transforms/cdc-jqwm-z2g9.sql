-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year and Quarter" AS year_and_quarter,
    "Topic" AS topic,
    "Indicator" AS indicator,
    "Time Period" AS time_period,
    CAST("Rate" AS DOUBLE) AS rate,
    "Unit" AS unit,
    "Significant" AS significant,
    "Standard Error" AS standard_error,
    "Footnote Symbol" AS footnote_symbol,
    "Footnote" AS footnote
FROM "cdc-jqwm-z2g9"
