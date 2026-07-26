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
    "OBJECTID" AS objectid,
    "PPIN" AS ppin,
    "NAME" AS name,
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
    "CD" AS cd,
    "SLDL" AS sldl,
    "SLDU" AS sldu,
    "SCHOOLYEAR" AS schoolyear
FROM "u-s-department-of-education-private-school-locations-current-6f472"
