-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows describe demographic and office attributes for institution reporting periods; filter by reporting date fields before comparing institutions over time.
SELECT
    "ID" AS id,
    CAST("CERT" AS BIGINT) AS cert,
    CAST("REPDTE" AS BIGINT) AS repdte,
    CAST("CALLYM" AS BIGINT) AS callym,
    "QTRNO" AS qtrno,
    "CBSANAME" AS cbsaname,
    "CNTRYALP" AS cntryalp,
    CAST("CNTYNUM" AS BIGINT) AS cntynum,
    CAST("MNRTYCDE" AS BIGINT) AS mnrtycde,
    CAST("MNRTYDTE" AS BIGINT) AS mnrtydte,
    "BRANCH" AS branch,
    "OFFTOT" AS offtot,
    "OFFNDOM" AS offndom,
    "OFFOTH" AS offoth,
    "OFFSTATE" AS offstate,
    "METRO" AS metro,
    "MICRO" AS micro,
    "DIVISION" AS division,
    "FDICTERR" AS fdicterr,
    "FDICAREA" AS fdicarea,
    "SIMS_LAT" AS sims_lat,
    "SIMS_LONG" AS sims_long
FROM "fdic-demographics"
