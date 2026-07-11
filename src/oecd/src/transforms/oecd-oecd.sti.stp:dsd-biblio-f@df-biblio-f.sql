-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "measure",
    "unit_measure",
    "origin",
    "destination",
    "decimals",
    "unit_mult",
    "value"
FROM "oecd-oecd.sti.stp:dsd-biblio-f@df-biblio-f"
