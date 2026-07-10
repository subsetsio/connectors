-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are annual aggregate rollups by state or FDIC geography; some state-year combinations appear more than once without a category discriminator in the raw endpoint, so preserve rows rather than assuming YEAR plus STALP is unique.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    "STALP" AS stalp,
    "STNAME" AS stname,
    "BANKS" AS banks,
    "OFFICES" AS offices,
    "BRANCHES" AS branches,
    "ASSET" AS asset,
    "DEP" AS dep,
    "DEPDOM" AS depdom,
    "LIAB" AS liab,
    "EQ" AS eq,
    "NETINC" AS netinc,
    "LNLS" AS lnls,
    "LNLSNET" AS lnlsnet,
    "NUMEMP" AS numemp,
    "TOTAL" AS total
FROM "fdic-summary"
