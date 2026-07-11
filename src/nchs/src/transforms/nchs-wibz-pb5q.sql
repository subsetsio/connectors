-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
SELECT
    "table",
    "select_setting",
    "value_type",
    "survey_year",
    "geography",
    "select_measure",
    "levels_of_measure",
    "value",
    "se",
    "low_95_ci",
    "high_95_ci",
    "footnote_value_cell",
    "footnote_measure_subscript",
    "value_with_footnote"
FROM "nchs-wibz-pb5q"
