-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("HUS_YEAR" AS BIGINT) AS hus_year,
    "HUS_SHORT_NAME" AS hus_short_name,
    "INDICATOR" AS indicator,
    CAST("PANEL_NUM" AS BIGINT) AS panel_num,
    "PANEL" AS panel,
    CAST("UNIT_NUM" AS BIGINT) AS unit_num,
    "UNIT" AS unit,
    CAST("STUB_NAME_NUM" AS BIGINT) AS stub_name_num,
    CAST("STUB_NAME_ORDER" AS BIGINT) AS stub_name_order,
    "STUB_NAME" AS stub_name,
    CAST("STUB_LABEL_NUM" AS BIGINT) AS stub_label_num,
    CAST("STUB_LABEL_ORDER" AS BIGINT) AS stub_label_order,
    "STUB_LABEL" AS stub_label,
    CAST("YEAR_NUM" AS BIGINT) AS year_num,
    CAST("YEAR" AS BIGINT) AS year,
    CAST("AGE_NUM" AS BIGINT) AS age_num,
    "AGE" AS age,
    CAST("ESTIMATE" AS DOUBLE) AS estimate,
    CAST("SE" AS DOUBLE) AS se,
    "FLAG" AS flag,
    "FOOTNOTE_ID_LIST" AS footnote_id_list,
    "FOOTNOTE_LIST" AS footnote_list
FROM "cdc-aewi-gwni"
