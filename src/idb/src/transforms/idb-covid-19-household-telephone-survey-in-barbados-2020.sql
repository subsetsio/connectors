-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("hhid" AS BIGINT) AS hhid,
    CAST("w_hh" AS DOUBLE) AS w_hh,
    CAST("psu" AS BIGINT) AS psu,
    CAST("stratum" AS BIGINT) AS stratum,
    "interview__key" AS interview_key,
    "interview__id" AS interview_id,
    CAST("spreading__id" AS BIGINT) AS spreading_id,
    CAST("optseq" AS BIGINT) AS optseq,
    "spropt",
    "sprdyn",
    "sprdyn_oth",
    "source_resource"
FROM "idb-covid-19-household-telephone-survey-in-barbados-2020"
