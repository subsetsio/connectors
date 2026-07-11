-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Reference-style source extract without a verified compact key; use the source columns as descriptive records rather than aggregating rows.
SELECT
    "resource_id",
    "resource_name",
    "DataZone" AS datazone,
    "DataZoneName" AS datazonename,
    "IntZone" AS intzone,
    "IntZoneName" AS intzonename,
    "CA" AS ca,
    "CAName" AS caname,
    "HSCP" AS hscp,
    "HSCPName" AS hscpname,
    "HB" AS hb,
    "HBName" AS hbname,
    "Country" AS country,
    strptime("CADateEnacted", '%Y%m%d')::DATE AS cadateenacted,
    strptime("CADateArchived", '%Y%m%d')::DATE AS cadatearchived,
    strptime("HSCPDateEnacted", '%Y%m%d')::DATE AS hscpdateenacted,
    strptime("HSCPDateArchived", '%Y%m%d')::DATE AS hscpdatearchived,
    strptime("HBDateEnacted", '%Y%m%d')::DATE AS hbdateenacted,
    strptime("HBDateArchived", '%Y%m%d')::DATE AS hbdatearchived,
    "ISDHBT" AS isdhbt,
    "ISDHBTName" AS isdhbtname,
    "CountryName" AS countryname
FROM "public-health-scotland-geography-codes-and-labels"
