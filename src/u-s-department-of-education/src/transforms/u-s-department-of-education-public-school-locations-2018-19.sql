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
    "010000500870|0100005|Albertville Middle School|01|600 E Alabama Ave|Albertville|AL|35950|01|01095|Marshall County|32|34.26019400000|-86.20617400000|10700|Albertville" AS 010000500870_0100005_albertville_middle_school_01_600_e_alabama_ave_albertville_al_35950_01_01095_marshall_county_32_34_26019400000_86_20617400000_10700_albertville,
    "AL|2|290|Huntsville-Decatur-Albertville" AS al_2_290_huntsville_decatur_albertville,
    "AL|N|N|0104|01026|01009|2018-2019" AS al_n_n_0104_01026_01009_2018_2019
FROM "u-s-department-of-education-public-school-locations-2018-19"
