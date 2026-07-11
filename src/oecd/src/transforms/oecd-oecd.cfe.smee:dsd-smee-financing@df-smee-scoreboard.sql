-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "sex_own",
    "entr_size",
    "transaction_type",
    "unit_measure",
    "prices",
    "obs_status",
    "unit_mult",
    "decimals",
    "country",
    "time_period",
    "value"
FROM "oecd-oecd.cfe.smee:dsd-smee-financing@df-smee-scoreboard"
