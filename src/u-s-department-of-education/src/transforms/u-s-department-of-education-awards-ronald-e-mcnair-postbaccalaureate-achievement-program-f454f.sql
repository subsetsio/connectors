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
    "PR Award Number" AS pr_award_number,
    "McNair Postbaccalaureate Achievement(McNr) Grantees" AS mcnair_postbaccalaureate_achievement_mcnr_grantees,
    "State" AS state,
    "Number of Participants" AS number_of_participants,
    "FY 2021 Funding (2021-22 Project Yr)" AS fy_2021_funding_2021_22_project_yr,
    "sheet_name",
    "McNair Postbaccalaureate Achievement (McNr) Grantees" AS mcnair_postbaccalaureate_achievement_mcnr_grantees_2,
    "FY 2020 Funding (2020-21 Project Yr)" AS fy_2020_funding_2020_21_project_yr,
    "FY 2019 Funding (2019-20 Project Yr)" AS fy_2019_funding_2019_20_project_yr,
    "FY 2018 Funding (2018-19 Project Yr)" AS fy_2018_funding_2018_19_project_yr,
    "McNair Postbaccalaureate Achievement (MCN) Grantees" AS mcnair_postbaccalaureate_achievement_mcn_grantees,
    "Number of Participants (Pending Verification)" AS number_of_participants_pending_verification,
    "FY 2017 Funding (2017-18 Project Yr)" AS fy_2017_funding_2017_18_project_yr,
    "FY 2016 Funding (2016-17 Project Yr)" AS fy_2016_funding_2016_17_project_yr,
    "McNair Postbaccalaureate Achievement (McN) Grantees_1" AS mcnair_postbaccalaureate_achievement_mcn_grantees_1,
    "FY 2015 Funding (2015-16 Project Yr)" AS fy_2015_funding_2015_16_project_yr,
    "Unnamed: 5" AS unnamed_5,
    "McNair Postbaccalaureate Achievement (McNair) Grantees" AS mcnair_postbaccalaureate_achievement_mcnair_grantees,
    "FY 2014 Funding (2014-15 Project Yr)" AS fy_2014_funding_2014_15_project_yr,
    "FY 2013 Funding (2013-14 Project Yr)" AS fy_2013_funding_2013_14_project_yr,
    "FY 2012 Funding (2012-13 Project Yr)" AS fy_2012_funding_2012_13_project_yr
FROM "u-s-department-of-education-awards-ronald-e-mcnair-postbaccalaureate-achievement-program-f454f"
