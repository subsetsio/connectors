-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are monthly fleet aggregates by flag state, gear type, and 0.1-degree grid cell; do not combine rows without preserving those aggregation dimensions.
SELECT
    "date",
    "year",
    "month",
    "cell_ll_lat",
    "cell_ll_lon",
    "flag",
    "geartype",
    "hours",
    "fishing_hours",
    "mmsi_present"
FROM "global-fishing-watch-fleet-monthly-10"
