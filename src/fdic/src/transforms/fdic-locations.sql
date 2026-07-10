-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Includes branches and offices tied to institutions; use service-type and status fields before treating every row as a currently operating branch.
SELECT
    CAST("CERT" AS BIGINT) AS cert,
    "NAME" AS name,
    CAST("UNINUM" AS BIGINT) AS uninum,
    "OFFNAME" AS offname,
    "OFFNUM" AS offnum,
    "MAINOFF" AS mainoff,
    "ADDRESS" AS address,
    "CITY" AS city,
    "STALP" AS stalp,
    "STNAME" AS stname,
    "ZIP" AS zip,
    "COUNTY" AS county,
    "SERVTYPE" AS servtype,
    "SERVTYPE_DESC" AS servtype_desc,
    strptime("ESTYMD", '%m/%d/%Y')::DATE AS estymd,
    strptime("ACQDATE", '%m/%d/%Y')::DATE AS acqdate,
    "CBSA_METRO_NAME" AS cbsa_metro_name,
    "LATITUDE" AS latitude,
    "LONGITUDE" AS longitude
FROM "fdic-locations"
