-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "AC_TYPEID" AS ac_typeid,
    CAST("AC_GROUP" AS BIGINT) AS ac_group,
    "SSD_NAME" AS ssd_name,
    "MANUFACTURER" AS manufacturer,
    "LONG_NAME" AS long_name,
    "SHORT_NAME" AS short_name,
    "BEGIN_DATE" AS begin_date,
    "END_DATE" AS end_date
FROM "bts-gdd"
