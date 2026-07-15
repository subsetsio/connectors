-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "MillionUSDollars" AS millionusdollars,
    "2013_Total" AS 2013_total,
    "2013_Export" AS 2013_export,
    "2013_Import" AS 2013_import,
    "2014_Total" AS 2014_total,
    "2014_Export" AS 2014_export,
    "2014_Import" AS 2014_import,
    "2015_Total" AS 2015_total,
    "2015_Export" AS 2015_export,
    "2015_Import" AS 2015_import,
    "2016_Total" AS 2016_total,
    "2016_Export" AS 2016_export,
    "2016_Import" AS 2016_import,
    "2017_Total" AS 2017_total,
    "2017_Export" AS 2017_export,
    "2017_Import" AS 2017_import,
    "2018_Total" AS 2018_total,
    "2018_Export" AS 2018_export,
    "2018_Import" AS 2018_import,
    "2019_Total" AS 2019_total,
    "2019_Export" AS 2019_export,
    "2019_Import" AS 2019_import,
    "2020_Total" AS 2020_total,
    "2020_Export" AS 2020_export,
    "2020_Import" AS 2020_import,
    "2021_Total" AS 2021_total,
    "2021_Export" AS 2021_export,
    "2021_Import" AS 2021_import,
    "2022_Total" AS 2022_total,
    "2022_Export" AS 2022_export,
    "2022_Import" AS 2022_import,
    "2023_Total" AS 2023_total,
    "2023_Export" AS 2023_export,
    "2023_Import" AS 2023_import
FROM "sg-data-d-8a9fb1409830202a0b06c222ffabc36a"
