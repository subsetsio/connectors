-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Summary of Deposits rows are annual branch-level observations; filter YEAR before aggregating deposits across branches or institutions.
SELECT
    "ID" AS id,
    CAST("CERT" AS BIGINT) AS cert,
    "NAMEFULL" AS namefull,
    "NAMEBR" AS namebr,
    CAST("YEAR" AS BIGINT) AS year,
    "STALPBR" AS stalpbr,
    "CITYBR" AS citybr,
    "CNTYNAMB" AS cntynamb,
    "ZIPBR" AS zipbr,
    "DEPSUMBR" AS depsumbr,
    "DEPSUM" AS depsum,
    "DEPDOM" AS depdom,
    "ASSET" AS asset,
    "BKCLASS" AS bkclass,
    "BRSERTYP" AS brsertyp,
    "BRNUM" AS brnum,
    "ADDRESBR" AS addresbr,
    "SIMS_LATITUDE" AS sims_latitude,
    "SIMS_LONGITUDE" AS sims_longitude
FROM "fdic-sod"
