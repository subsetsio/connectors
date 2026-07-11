-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Reference-style source extract without a verified compact key; use the source columns as descriptive records rather than aggregating rows.
SELECT
    "resource_id",
    "resource_name",
    "SHB" AS shb,
    "SHBName" AS shbname,
    "Country" AS country,
    "StrategicBusinessUnit" AS strategicbusinessunit,
    "StrategicBusinessUnitName" AS strategicbusinessunitname,
    "GroupedGeography" AS groupedgeography,
    "GroupedGeographyName" AS groupedgeographyname,
    "GroupedGeographyDetails" AS groupedgeographydetails,
    "CustomResidency" AS customresidency,
    "CustomResidencyName" AS customresidencyname
FROM "public-health-scotland-non-standard-geography-codes-and-labels"
