-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: House returns span many election years, districts, parties, and candidates; filter to a single year and district scope before aggregating.
SELECT
    "year",
    "state",
    "state_po",
    "state_fips",
    "state_cen",
    "state_ic",
    "office",
    "district",
    "stage",
    "runoff"
FROM "mit-election-lab-dvn-ig0un2"
