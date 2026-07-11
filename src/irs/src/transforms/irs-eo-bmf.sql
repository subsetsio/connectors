-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is the current Business Master File snapshot, not a filing history; financial return tables carry annual filing facts.
SELECT
    "ein",
    "name",
    "ico",
    "street",
    "city",
    "state",
    "zip",
    "group",
    "subsection",
    CAST("affiliation" AS BIGINT) AS affiliation,
    "classification",
    "ruling",
    CAST("deductibility" AS BIGINT) AS deductibility,
    "foundation",
    "activity",
    CAST("organization" AS BIGINT) AS organization,
    "status",
    CAST("tax_period" AS BIGINT) AS tax_period,
    CAST("asset_cd" AS BIGINT) AS asset_cd,
    CAST("income_cd" AS BIGINT) AS income_cd,
    "filing_req_cd",
    CAST("pf_filing_req_cd" AS BIGINT) AS pf_filing_req_cd,
    "acct_pd",
    "ntee_cd",
    "sort_name",
    "asset_amt",
    "income_amt",
    "revenue_amt"
FROM "irs-eo-bmf"
