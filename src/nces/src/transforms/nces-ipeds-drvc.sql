-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("UNITID" AS BIGINT) AS unitid,
    CAST("ASCDEG" AS BIGINT) AS ascdeg,
    "BASDEG" AS basdeg,
    "MASDEG" AS masdeg,
    "DOCDEGRS" AS docdegrs,
    "DOCDEGPP" AS docdegpp,
    "DOCDEGOT" AS docdegot,
    CAST("CERT1" AS BIGINT) AS cert1,
    CAST("CERT1A" AS BIGINT) AS cert1a,
    CAST("CERT1B" AS BIGINT) AS cert1b,
    CAST("CERT2" AS BIGINT) AS cert2,
    CAST("CERT4" AS BIGINT) AS cert4,
    "PBACERT" AS pbacert,
    "PMACERT" AS pmacert,
    CAST("SASCDEG" AS BIGINT) AS sascdeg,
    "SBASDEG" AS sbasdeg,
    "SMASDEG" AS smasdeg,
    "SDOCDEG" AS sdocdeg,
    CAST("SCERT1A" AS BIGINT) AS scert1a,
    CAST("SCERT1B" AS BIGINT) AS scert1b,
    CAST("SCERT24" AS BIGINT) AS scert24,
    "SBAMACRT" AS sbamacrt,
    "year"
FROM "nces-ipeds-drvc"
