-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "location",
    "subject",
    "measure",
    "frequency",
    "obs_status",
    "unit_measure",
    "unit_mult",
    "base_per",
    "time_period",
    "value"
FROM "oecd-oecd.sdd.sdps:df-test-mei"
