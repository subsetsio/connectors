-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: QCT and DDA designations are annual eligibility/reference designations; compare within a fiscal year before using them as a geography lookup.
SELECT
    CAST("cbsa" AS BIGINT) AS cbsa,
    "statefp",
    "cnty",
    "stcnty",
    "tract",
    CAST("splittr" AS BIGINT) AS splittr,
    "qct_id",
    "fips",
    "fiscal_year"
FROM "hud-qct-dda"
