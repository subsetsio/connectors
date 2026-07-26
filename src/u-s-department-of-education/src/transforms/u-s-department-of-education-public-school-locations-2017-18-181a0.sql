-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Catalog-level dataset may contain mixed measures, geography levels, or reporting periods; inspect column definitions before aggregating.
SELECT
    "package_id",
    "package_title",
    "resource_id",
    "resource_name",
    "resource_format",
    "resource_position",
    "row_number",
    "X" AS x,
    "Y" AS y,
    "NCESSCH" AS ncessch,
    "NAME" AS name,
    "OPSTFIPS" AS opstfips,
    "STREET" AS street,
    "CITY" AS city,
    "STATE" AS state,
    "ZIP" AS zip,
    "STFIP" AS stfip,
    "CNTY" AS cnty,
    "NMCNTY" AS nmcnty,
    "LOCALE" AS locale,
    "LAT" AS lat,
    "LON" AS lon,
    "CBSA" AS cbsa,
    "NMCBSA" AS nmcbsa,
    "CBSATYPE" AS cbsatype,
    "CSA" AS csa,
    "NMCSA" AS nmcsa,
    "NECTA" AS necta,
    "NMNECTA" AS nmnecta,
    "CD" AS cd,
    "SLDL" AS sldl,
    "SLDU" AS sldu,
    "SCHOOLYEAR" AS schoolyear,
    "OBJECTID" AS objectid
FROM "u-s-department-of-education-public-school-locations-2017-18-181a0"
