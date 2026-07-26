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
    "LEAID" AS leaid,
    "OPSTFIPS" AS opstfips,
    "LSTREE" AS lstree,
    "LCITY" AS lcity,
    "LSTATE" AS lstate,
    "LZIP" AS lzip,
    "LZIP4" AS lzip4,
    "STFIP15" AS stfip15,
    "CNTY15" AS cnty15,
    "NMCNTY15" AS nmcnty15,
    "LAT1516" AS lat1516,
    "LON1516" AS lon1516,
    "CBSA15" AS cbsa15,
    "NMCBSA15" AS nmcbsa15,
    "CBSATYPE15" AS cbsatype15,
    "CSA15" AS csa15,
    "NMCSA15" AS nmcsa15,
    "NECTA15" AS necta15,
    "NMNECTA15" AS nmnecta15,
    "CD15" AS cd15,
    "SLDL15" AS sldl15,
    "SLDU15" AS sldu15,
    "NAME" AS name,
    "archive_member",
    "sheet_name"
FROM "u-s-department-of-education-school-district-office-locations-2015-16-64181"
