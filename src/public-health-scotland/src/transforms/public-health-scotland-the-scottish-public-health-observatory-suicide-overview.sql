-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    CAST("Year" AS BIGINT) AS year,
    "HBR" AS hbr,
    "HBRQF" AS hbrqf,
    "Sex" AS sex,
    "SexQF" AS sexqf,
    CAST("IndividualsCount" AS BIGINT) AS individualscount,
    "CA" AS ca,
    "CAQF" AS caqf,
    "TimeRange" AS timerange,
    "SIMDDecile" AS simddecile,
    "SIMDDecileQF" AS simddecileqf,
    CAST("CrudeRate" AS DOUBLE) AS cruderate,
    "CrudeRateQF" AS cruderateqf
FROM "public-health-scotland-the-scottish-public-health-observatory-suicide-overview"
