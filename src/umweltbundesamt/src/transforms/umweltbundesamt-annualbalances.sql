-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains pre-aggregated annual statistics by station, pollutant component, and averaging scope; do not combine rows across scopes or components without filtering or grouping by those dimensions.
SELECT
    "component_id",
    "scope_id",
    "year",
    "station_id",
    "annual_mean",
    "exceedance_days",
    "extra_value"
FROM "umweltbundesamt-annualbalances"
