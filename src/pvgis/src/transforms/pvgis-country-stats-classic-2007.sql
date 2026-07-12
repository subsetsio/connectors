-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The country_code column includes both geography codes and workbook summary rows such as minimum, maximum, and country-average statistics; country_name is only populated for geography rows. Filter the desired row type before aggregating values.
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
FROM "pvgis-country-stats-classic-2007"
