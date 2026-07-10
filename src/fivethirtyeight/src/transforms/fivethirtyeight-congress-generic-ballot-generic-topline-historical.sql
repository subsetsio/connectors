-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "subgroup",
    "modeldate",
    "dem_estimate",
    "dem_hi",
    "dem_lo",
    "rep_estimate",
    "rep_hi",
    "rep_lo",
    "timestamp"
FROM "fivethirtyeight-congress-generic-ballot-generic-topline-historical"
