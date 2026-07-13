-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("hhid" AS BIGINT) AS hhid,
    CAST("weight2020" AS DOUBLE) AS weight2020,
    CAST("psu" AS BIGINT) AS psu,
    CAST("stratum" AS BIGINT) AS stratum,
    CAST("great_par" AS BIGINT) AS great_par,
    CAST("district" AS BIGINT) AS district,
    CAST("spreading__id" AS BIGINT) AS spreading_id,
    CAST("optseq" AS BIGINT) AS optseq,
    "spropt_eng",
    "spropt_nld",
    "spropt_srn",
    "sprdyn",
    "source_resource"
FROM "idb-suriname-covid-19-survey-2020"
