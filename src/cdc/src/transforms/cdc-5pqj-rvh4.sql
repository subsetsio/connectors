-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "stat_group",
    "stat_var",
    "Outcome (or Indicator)" AS outcome_or_indicator,
    "row_group",
    "row_var",
    "row_label",
    "rowLevels" AS rowlevels,
    "col_group",
    "col_var",
    "col_label",
    "Group" AS group,
    CAST("Percentage" AS DOUBLE) AS percentage,
    "Confidence Interval" AS confidence_interval,
    "Title" AS title,
    "Description" AS description,
    "new_caption2",
    CAST("FIGURE" AS BIGINT) AS figure,
    CAST("CR_P_RELIABLE" AS BIGINT) AS cr_p_reliable,
    CAST("CR_Q_RELIABLE" AS BIGINT) AS cr_q_reliable,
    CAST("ZERO" AS BIGINT) AS zero,
    "KG_FLAG" AS kg_flag,
    "Date Range" AS date_range
FROM "cdc-5pqj-rvh4"
