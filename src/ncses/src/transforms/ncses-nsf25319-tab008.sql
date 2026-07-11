-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Type of institution" AS type_of_institution,
    "Started in FY 2006 or FY 2007 - Number of institutions" AS started_in_fy_2006_or_fy_2007_number_of_institutions,
    "Started in FY 2006 or FY 2007 - Total NASF" AS started_in_fy_2006_or_fy_2007_total_nasf,
    "Started in FY 2008 or FY 2009 - Number of institutions" AS started_in_fy_2008_or_fy_2009_number_of_institutions,
    "Started in FY 2008 or FY 2009 - Total NASF" AS started_in_fy_2008_or_fy_2009_total_nasf,
    "Started in FY 2010 or FY 2011 - Number of institutions" AS started_in_fy_2010_or_fy_2011_number_of_institutions,
    "Started in FY 2010 or FY 2011 - Total NASF" AS started_in_fy_2010_or_fy_2011_total_nasf,
    "Started in FY 2012 or FY 2013 - Number of institutions" AS started_in_fy_2012_or_fy_2013_number_of_institutions,
    "Started in FY 2012 or FY 2013 - Total NASF" AS started_in_fy_2012_or_fy_2013_total_nasf,
    "Started in FY 2014 or FY 2015 - Number of institutions" AS started_in_fy_2014_or_fy_2015_number_of_institutions,
    "Started in FY 2014 or FY 2015 - Total NASF" AS started_in_fy_2014_or_fy_2015_total_nasf,
    "Started in FY 2016 or FY 2017 - Number of institutions" AS started_in_fy_2016_or_fy_2017_number_of_institutions,
    "Started in FY 2016 or FY 2017 - Total NASF" AS started_in_fy_2016_or_fy_2017_total_nasf,
    "Started in FY 2018 or FY 2019 - Number of institutions" AS started_in_fy_2018_or_fy_2019_number_of_institutions,
    "Started in FY 2018 or FY 2019 - Total NASF" AS started_in_fy_2018_or_fy_2019_total_nasf,
    "Started in FY 2020 or FY 2021 - Number of institutions" AS started_in_fy_2020_or_fy_2021_number_of_institutions,
    "Started in FY 2020 or FY 2021 - Total NASF" AS started_in_fy_2020_or_fy_2021_total_nasf,
    "Started in FY 2022 or FY 2023 - Number of institutions" AS started_in_fy_2022_or_fy_2023_number_of_institutions,
    "Started in FY 2022 or FY 2023 - Total NASF" AS started_in_fy_2022_or_fy_2023_total_nasf,
    "Planned to start in FY 2024 or FY 2025 - Number of institutions" AS planned_to_start_in_fy_2024_or_fy_2025_number_of_institutions,
    "Planned to start in FY 2024 or FY 2025 - Total NASF" AS planned_to_start_in_fy_2024_or_fy_2025_total_nasf
FROM "ncses-nsf25319-tab008"
