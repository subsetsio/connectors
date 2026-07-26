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
    "sheet_name",
    "row_number",
    "PR Award Number" AS pr_award_number,
    "Upward Bound-Veterans(VUB) Grantees" AS upward_bound_veterans_vub_grantees,
    "State" AS state,
    "Number of Participants" AS number_of_participants,
    "FY 2021 Funding (2021-22 Project Yr)" AS fy_2021_funding_2021_22_project_yr,
    "Unnamed: 5" AS unnamed_5,
    "Upward Bound-Veterans (VUB) Grantees" AS upward_bound_veterans_vub_grantees_2,
    "FY 2020 Funding (2020-21 Project Yr)" AS fy_2020_funding_2020_21_project_yr,
    "FY 2019 Funding (2019-20 Project Yr)" AS fy_2019_funding_2019_20_project_yr,
    "FY 2018 Funding (2018-19 Project Yr)" AS fy_2018_funding_2018_19_project_yr,
    "Number of Participants (Pending Verification)" AS number_of_participants_pending_verification,
    "FY 2017 Funding (2017-18 Project Yr)" AS fy_2017_funding_2017_18_project_yr,
    "FY 2016 Funding (2016-17 Project Yr)" AS fy_2016_funding_2016_17_project_yr,
    "FY 2015 Funding (2015-16 Project Yr)" AS fy_2015_funding_2015_16_project_yr,
    "FY 2014 Funding (2014-15 Project Yr)" AS fy_2014_funding_2014_15_project_yr,
    "FY 2013 Funding (2013-14 Project Yr)" AS fy_2013_funding_2013_14_project_yr,
    "Veterans Upward Bound (VUB) Grantees" AS veterans_upward_bound_vub_grantees,
    "FY 2012 Funding (2012-13 Project Yr)" AS fy_2012_funding_2012_13_project_yr,
    "FY 2011 Funding (2011-12 Project Yr)" AS fy_2011_funding_2011_12_project_yr
FROM "u-s-department-of-education-awards-veterans-upward-bound-program-4cabf"
