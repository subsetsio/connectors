-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TOPIC" AS topic,
    "SUBTOPIC" AS subtopic,
    "SUBTOPIC_ID" AS subtopic_id,
    "TAXONOMY" AS taxonomy,
    CAST("TAXONOMY_ID" AS BIGINT) AS taxonomy_id,
    "CLASSIFICATION" AS classification,
    CAST("CLASSIFICATION_ID" AS BIGINT) AS classification_id,
    "GROUP" AS group,
    CAST("GROUP_ID" AS BIGINT) AS group_id,
    CAST("GROUP_ORDER" AS BIGINT) AS group_order,
    "SUBGROUP" AS subgroup,
    CAST("SUBGROUP_ID" AS BIGINT) AS subgroup_id,
    CAST("SUBGROUP_ORDER" AS BIGINT) AS subgroup_order,
    "NESTING_LABEL" AS nesting_label,
    CAST("NESTING_LABEL_ID" AS BIGINT) AS nesting_label_id,
    "ESTIMATE_TYPE" AS estimate_type,
    CAST("ESTIMATE_TYPE_ID" AS BIGINT) AS estimate_type_id,
    "TIME_PERIOD" AS time_period,
    CAST("TIME_PERIOD_ID" AS BIGINT) AS time_period_id,
    CAST("ESTIMATE" AS DOUBLE) AS estimate,
    CAST("STANDARD_ERROR" AS DOUBLE) AS standard_error,
    CAST("ESTIMATE_LCI" AS DOUBLE) AS estimate_lci,
    CAST("ESTIMATE_UCI" AS DOUBLE) AS estimate_uci,
    "FLAG" AS flag,
    "FOOTNOTE_ID_LIST" AS footnote_id_list
FROM "cdc-6rvp-rahv"
