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
    "archive_member",
    "row_number",
    "010000200277",
    "Sequoyah Sch - Chalkville Campus" AS sequoyah_sch_chalkville_campus,
    "01",
    "1000 Industrial School Road" AS 1000_industrial_school_road,
    "Birmingham" AS birmingham,
    "AL" AS al,
    "35220",
    "01.1" AS 01_1,
    "01073",
    "Jefferson County" AS jefferson_county,
    "21",
    "33.67366100000" AS 33_67366100000,
    "-86.62875500000" AS 86_62875500000,
    "13820",
    "Birmingham-Hoover, AL" AS birmingham_hoover_al,
    "1",
    "142",
    "Birmingham-Hoover-Talladega, AL" AS birmingham_hoover_talladega_al,
    "N" AS n,
    "N.1" AS n_1,
    "0106",
    "01044",
    "01020",
    "2016"
FROM "u-s-department-of-education-public-school-locations-2016-17"
