-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Includes active and inactive institutions; filter status and closing-date fields when analyzing the current institution universe.
SELECT
    CAST("CERT" AS BIGINT) AS cert,
    "NAME" AS name,
    "CITY" AS city,
    "STALP" AS stalp,
    "STNAME" AS stname,
    "ZIP" AS zip,
    "COUNTY" AS county,
    "ADDRESS" AS address,
    "BKCLASS" AS bkclass,
    CAST("CHARTER" AS BIGINT) AS charter,
    "CHRTAGNT" AS chrtagnt,
    "REGAGNT" AS regagnt,
    CAST("FED_RSSD" AS BIGINT) AS fed_rssd,
    CAST("UNINUM" AS BIGINT) AS uninum,
    "ACTIVE" AS active,
    strptime("ESTYMD", '%m/%d/%Y')::DATE AS estymd,
    strptime("ENDEFYMD", '%m/%d/%Y')::DATE AS endefymd,
    strptime("INSDATE", '%m/%d/%Y')::DATE AS insdate,
    "WEBADDR" AS webaddr,
    "MDI_STATUS_DESC" AS mdi_status_desc,
    "CBSA_METRO_NAME" AS cbsa_metro_name,
    "CSA" AS csa,
    strptime("RISDATE", '%m/%d/%Y')::DATE AS risdate,
    "LATITUDE" AS latitude,
    "LONGITUDE" AS longitude
FROM "fdic-institutions"
