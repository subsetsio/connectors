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
    "010000500870|0100005|Albertville Middle School|01|600 E Alabama Ave|Albertville|AL|35950|01|01095|Marshall County|32|34.260200|-86.206200|10700|Albertville" AS 010000500870_0100005_albertville_middle_school_01_600_e_alabama_ave_albertville_al_35950_01_01095_marshall_county_32_34_260200_86_206200_10700_albertville,
    "AL|2|N|N|N|N|0104|01026|01009|2021-2022" AS al_2_n_n_n_n_0104_01026_01009_2021_2022
FROM "u-s-department-of-education-public-school-locations-2021-22"
