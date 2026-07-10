-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "INDICATOR" AS indicator,
    CAST("INDICATOR_NUM" AS BIGINT) AS indicator_num,
    "UNIT" AS unit,
    CAST("UNIT_NUM" AS BIGINT) AS unit_num,
    "STUB_NAME" AS stub_name,
    CAST("STUB_NAME_NUM" AS BIGINT) AS stub_name_num,
    "STUB_LABEL" AS stub_label,
    CAST("STUB_LABEL_NUM" AS DOUBLE) AS stub_label_num,
    CAST("YEAR" AS BIGINT) AS year,
    CAST("YEAR_NUM" AS BIGINT) AS year_num,
    CAST("ESTIMATE" AS DOUBLE) AS estimate,
    "FLAG" AS flag
FROM "cdc-nfuu-hu6j"
