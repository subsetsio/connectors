-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Type of institution" AS type_of_institution,
    "Started in FY 2006 or FY 2007 - Costs" AS started_in_fy_2006_or_fy_2007_costs,
    "Started in FY 2006 or FY 2007 - NASF" AS started_in_fy_2006_or_fy_2007_nasf,
    "Started in FY 2008 or FY 2009 - Costs" AS started_in_fy_2008_or_fy_2009_costs,
    "Started in FY 2008 or FY 2009 - NASF" AS started_in_fy_2008_or_fy_2009_nasf,
    "Started in FY 2010 or FY 2011 - Costs" AS started_in_fy_2010_or_fy_2011_costs,
    "Started in FY 2010 or FY 2011 - NASF" AS started_in_fy_2010_or_fy_2011_nasf,
    "Started in FY 2012 or FY 2013 - Costs" AS started_in_fy_2012_or_fy_2013_costs,
    "Started in FY 2012 or FY 2013 - NASF" AS started_in_fy_2012_or_fy_2013_nasf,
    "Started in FY 2014 or FY 2015 - Costs" AS started_in_fy_2014_or_fy_2015_costs,
    "Started in FY 2014 or FY 2015 - NASF" AS started_in_fy_2014_or_fy_2015_nasf,
    "Started in FY 2016 or FY 2017 - Costs" AS started_in_fy_2016_or_fy_2017_costs,
    "Started in FY 2016 or FY 2017 - NASF" AS started_in_fy_2016_or_fy_2017_nasf,
    "Started in FY 2018 or FY 2019 - Costs" AS started_in_fy_2018_or_fy_2019_costs,
    "Started in FY 2018 or FY 2019 - NASF" AS started_in_fy_2018_or_fy_2019_nasf,
    "Started in FY 2020 or FY 2021 - Costs" AS started_in_fy_2020_or_fy_2021_costs,
    "Started in FY 2020 or FY 2021 - NASF" AS started_in_fy_2020_or_fy_2021_nasf,
    "Started in FY 2022 or FY 2023 - Costs" AS started_in_fy_2022_or_fy_2023_costs,
    "Started in FY 2022 or FY 2023 - NASF" AS started_in_fy_2022_or_fy_2023_nasf,
    "Planned to start in FY 2024 or FY 2025 - Costs" AS planned_to_start_in_fy_2024_or_fy_2025_costs,
    "Planned to start in FY 2024 or FY 2025 - NASF" AS planned_to_start_in_fy_2024_or_fy_2025_nasf,
    "Costs of deferred projects - Included in institutional plan" AS costs_of_deferred_projects_included_in_institutional_plan,
    "Costs of deferred projects - Not included in institutional plan" AS costs_of_deferred_projects_not_included_in_institutional_plan
FROM "ncses-nsf25319-tab014"
