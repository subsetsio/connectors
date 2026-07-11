-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Type of institution" AS type_of_institution,
    "Started in FY 2006 or FY 2007" AS started_in_fy_2006_or_fy_2007,
    "Started in FY 2008 or FY 2009" AS started_in_fy_2008_or_fy_2009,
    "Started in FY 2010 or FY 2011" AS started_in_fy_2010_or_fy_2011,
    "Started in FY 2012 or FY 2013" AS started_in_fy_2012_or_fy_2013,
    "Started in FY 2014 or FY 2015" AS started_in_fy_2014_or_fy_2015,
    "Started in FY 2016 or FY 2017" AS started_in_fy_2016_or_fy_2017,
    "Started in FY 2018 or FY 2019" AS started_in_fy_2018_or_fy_2019,
    "Started in FY 2020 or FY 2021" AS started_in_fy_2020_or_fy_2021,
    "Started in FY 2022 or FY 2023" AS started_in_fy_2022_or_fy_2023
FROM "ncses-nsf25319-tab013"
