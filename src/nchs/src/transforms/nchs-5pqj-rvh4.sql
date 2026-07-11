-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
SELECT
    "stat_group",
    "stat_var",
    "outcome_or_indicator",
    "row_group",
    "row_var",
    "row_label",
    "rowlevels",
    "col_group",
    "col_var",
    "col_label",
    "group",
    "percentage",
    "confidence_interval",
    "title",
    "description",
    "new_caption2",
    "figure",
    "cr_p_reliable",
    "cr_q_reliable",
    "zero",
    "kg_flag",
    "date_range"
FROM "nchs-5pqj-rvh4"
