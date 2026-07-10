-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are institution-period financial observations; aggregate only after choosing a reporting period to avoid summing across quarters.
SELECT
    CAST("CERT" AS BIGINT) AS cert,
    "NAME" AS name,
    CAST("REPDTE" AS BIGINT) AS repdte,
    strptime("RISDATE", '%Y%m%d')::DATE AS risdate,
    "STALP" AS stalp,
    "CITY" AS city,
    "BKCLASS" AS bkclass,
    "ASSET" AS asset,
    "DEP" AS dep,
    "DEPDOM" AS depdom,
    "DEPINS" AS depins,
    "DEPUNINS" AS depunins,
    "LIAB" AS liab,
    "EQ" AS eq,
    "EQTOT" AS eqtot,
    "NETINC" AS netinc,
    "ROA" AS roa,
    "ROE" AS roe,
    "NIM" AS nim,
    "NUMEMP" AS numemp,
    "LNLSNET" AS lnlsnet,
    "INTINC" AS intinc,
    "INTEXPY" AS intexpy
FROM "fdic-financials"
