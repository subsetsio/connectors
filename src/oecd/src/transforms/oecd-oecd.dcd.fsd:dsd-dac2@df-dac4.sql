-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "donor",
    "recipient",
    "measure",
    "unit_measure",
    "price_base",
    "base_per",
    "unit_mult",
    "flow_type",
    "obs_status",
    "time_period",
    "value"
FROM "oecd-oecd.dcd.fsd:dsd-dac2@df-dac4"
