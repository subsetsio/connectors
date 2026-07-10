-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are structure-change events, so one institution can appear many times as its charter, location, ownership, or status changes.
SELECT
    "ID" AS id,
    CAST("CERT" AS BIGINT) AS cert,
    "INSTNAME" AS instname,
    CAST("CHANGECODE" AS BIGINT) AS changecode,
    "CHANGECODE_DESC" AS changecode_desc,
    CAST("EFFDATE" AS TIMESTAMP) AS effdate,
    CAST("EFFYEAR" AS BIGINT) AS effyear,
    CAST("PROCDATE" AS TIMESTAMP) AS procdate,
    "CLASS" AS class,
    "CLASS_TYPE_DESC" AS class_type_desc,
    "PCITY" AS pcity,
    "PSTALP" AS pstalp,
    CAST("TRANSNUM" AS BIGINT) AS transnum,
    "FDICREGION_DESC" AS fdicregion_desc,
    "ORGTYPE" AS orgtype
FROM "fdic-history"
