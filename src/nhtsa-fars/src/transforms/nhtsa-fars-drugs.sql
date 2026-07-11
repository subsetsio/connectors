-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Drug test rows can contain multiple test/result observations per person; do not aggregate as one row per person.
SELECT
    CAST("STATE" AS BIGINT) AS state,
    "STATENAME" AS statename,
    CAST("ST_CASE" AS BIGINT) AS st_case,
    CAST("VEH_NO" AS BIGINT) AS veh_no,
    CAST("PER_NO" AS BIGINT) AS per_no,
    CAST("DRUGSPEC" AS BIGINT) AS drugspec,
    "DRUGSPECNAME" AS drugspecname,
    CAST("DRUGRES" AS BIGINT) AS drugres,
    "DRUGRESNAME" AS drugresname,
    CAST("DRUGMETHOD" AS BIGINT) AS drugmethod,
    "DRUGMETHODNAME" AS drugmethodname,
    CAST("DRUGQTY" AS BIGINT) AS drugqty,
    "DRUGQTYNAME" AS drugqtyname,
    CAST("DRUGACTQTY" AS DOUBLE) AS drugactqty,
    "DRUGACTQTYNAME" AS drugactqtyname,
    CAST("DRUGUOM" AS BIGINT) AS druguom,
    "DRUGUOMNAME" AS druguomname,
    "case_year"
FROM "nhtsa-fars-drugs"
