-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "sector",
    "pct",
    "patrol_bor",
    "sq_miles",
    "nco_phase",
    "sector_ind"
FROM "nyc-open-data-5rqd-h5ci"
