-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    CAST("Year" AS BIGINT) AS year,
    "Month" AS month,
    "Period" AS period,
    "Indicator" AS indicator,
    CAST("Data Value" AS BIGINT) AS data_value,
    CAST("Percent Complete" AS DOUBLE) AS percent_complete,
    CAST("Percent Pending Investigation" AS DOUBLE) AS percent_pending_investigation,
    "State Name" AS state_name,
    "Footnote" AS footnote,
    "Footnote Symbol" AS footnote_symbol,
    CAST("Predicted Value" AS BIGINT) AS predicted_value
FROM "cdc-xkb8-kh2a"
