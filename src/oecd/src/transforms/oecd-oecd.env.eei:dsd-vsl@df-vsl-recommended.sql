-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "source_derivation",
    "methodology",
    "income_elasticity",
    "unit_measure",
    "statistical_operation",
    "base_per",
    "measure_vsl",
    "obs_status",
    "unit_mult",
    "prices",
    "value"
FROM "oecd-oecd.env.eei:dsd-vsl@df-vsl-recommended"
