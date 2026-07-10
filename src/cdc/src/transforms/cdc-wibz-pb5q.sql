-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Table" AS BIGINT) AS table,
    "Select Setting" AS select_setting,
    "Value type" AS value_type,
    CAST("Survey Year" AS BIGINT) AS survey_year,
    "Geography" AS geography,
    "Select Measure" AS select_measure,
    "Levels of Measure" AS levels_of_measure,
    CAST("Value" AS DOUBLE) AS value,
    CAST("SE" AS DOUBLE) AS se,
    CAST("Low 95% CI" AS DOUBLE) AS low_95_ci,
    CAST("High 95% CI" AS DOUBLE) AS high_95_ci,
    "Footnote-Value cell" AS footnote_value_cell,
    "Footnote-Measure Subscript" AS footnote_measure_subscript,
    "Value with Footnote" AS value_with_footnote
FROM "cdc-wibz-pb5q"
