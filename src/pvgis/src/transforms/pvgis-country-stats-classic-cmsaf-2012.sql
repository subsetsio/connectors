-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The geography columns include country and regional entries from the PVGIS workbook; filter the desired geography before aggregating values.
SELECT
    "source_file",
    "workbook_version",
    "methodology",
    "sheet",
    "country_code",
    "country_name",
    "metric_group",
    "statistic",
    "value"
FROM "pvgis-country-stats-classic-cmsaf-2012"
