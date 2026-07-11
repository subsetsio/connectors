-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "State or territory control and institution - Alabama - Public" AS state_or_territory_control_and_institution_alabama_public,
    "Started in FY 2006 or FY 2007 - Alabama - Public" AS started_in_fy_2006_or_fy_2007_alabama_public,
    "Started in FY 2008 or FY 2009 - Alabama - Public" AS started_in_fy_2008_or_fy_2009_alabama_public,
    "Started in FY 2010 or FY 2011 - Alabama - Public" AS started_in_fy_2010_or_fy_2011_alabama_public,
    "Started in FY 2012 or FY 2013 - Alabama - Public" AS started_in_fy_2012_or_fy_2013_alabama_public,
    "Started in FY 2014 or FY 2015 - Alabama - Public" AS started_in_fy_2014_or_fy_2015_alabama_public,
    "Started in FY 2016 or FY 2017 - Alabama - Public" AS started_in_fy_2016_or_fy_2017_alabama_public,
    "Started in FY 2018 or FY 2019 - Alabama - Public" AS started_in_fy_2018_or_fy_2019_alabama_public,
    "Started in FY 2020 or FY 2021 - Alabama - Public" AS started_in_fy_2020_or_fy_2021_alabama_public,
    "Started in FY 2022 or FY 2023 - Alabama - Public" AS started_in_fy_2022_or_fy_2023_alabama_public,
    "Planned to start in FY 2024 or FY 2025 - Alabama - Public" AS planned_to_start_in_fy_2024_or_fy_2025_alabama_public,
    "Deferred projects - Included in institutional plan - Alabama - Public" AS deferred_projects_included_in_institutional_plan_alabama_public,
    "Deferred projects - Not included in institutional plan - Alabama - Public" AS deferred_projects_not_included_in_institutional_plan_alabama_public
FROM "ncses-nsf25319-tab017"
