-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "DataZone" AS datazone,
    "SubHSCPName" AS subhscpname,
    "CA" AS ca,
    "HSCP" AS hscp,
    "HB" AS hb,
    "Country" AS country
FROM "public-health-scotland-sub-health-and-social-care-partnership-areas"
