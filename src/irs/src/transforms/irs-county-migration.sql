-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Inflow and outflow files describe directional migration perspectives; filter direction before aggregating flows to avoid double counting paired perspectives.
-- caution: Some migration rows represent suppressed, non-US, or aggregate origin/destination buckets without complete FIPS codes.
SELECT
    "year",
    "direction",
    "y2_statefips",
    "y2_countyfips",
    "y1_statefips",
    "y1_countyfips",
    "y1_state",
    "y1_countyname",
    "n1",
    "n2",
    "agi"
FROM "irs-county-migration"
