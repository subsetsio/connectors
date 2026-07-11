-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Type of cost highest degree granted and institutional control - All institutions" AS type_of_cost_highest_degree_granted_and_institutional_control_all_institutions,
    "2010 - All institutions" AS 2010_all_institutions,
    "2011 - All institutions" AS 2011_all_institutions,
    "2012 - All institutions" AS 2012_all_institutions,
    "2013 - All institutions" AS 2013_all_institutions,
    "2014 - All institutions" AS 2014_all_institutions,
    "2015 - All institutions" AS 2015_all_institutions,
    "2016 - All institutions" AS 2016_all_institutions,
    "2017 - All institutions" AS 2017_all_institutions,
    "2018 - All institutions" AS 2018_all_institutions,
    "2019 - All institutions" AS 2019_all_institutions,
    "2020 - All institutions" AS 2020_all_institutions,
    "2021 - All institutions" AS 2021_all_institutions,
    "2022 - All institutions" AS 2022_all_institutions,
    "2023 - All institutions" AS 2023_all_institutions,
    "2024 - All institutions" AS 2024_all_institutions
FROM "ncses-nsf26304-tab012"
