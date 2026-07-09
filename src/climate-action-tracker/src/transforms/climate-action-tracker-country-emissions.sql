-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include historical emissions, current-policy pathway bounds, NDC targets, fair-share and modelled-domestic-pathway boundaries, and warming-rating scenario lines; filter scenario, sector, indicator, and variable before aggregating.
-- caution: The sector column includes economy-wide values excluding LULUCF and separate LULUCF rows, so summing sectors can double-count unless the desired sector scope is selected first.
SELECT
    "id",
    "variable",
    "per_capita",
    "region",
    "scenario",
    "sector",
    "indicator",
    "year",
    "value",
    "unit",
    "version",
    "version_date",
    "comments",
    "source",
    "edition"
FROM "climate-action-tracker-country-emissions"
