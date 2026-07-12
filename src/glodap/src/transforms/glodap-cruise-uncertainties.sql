-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "expocode",
    "oxygen_pct",
    "nitrate_pct",
    "phosphate_pct",
    "silicate_pct",
    "tco2_umol_kg",
    "talk_umol_kg",
    "salinity",
    "cfc11_pct",
    "cfc12_pct",
    "cfc113_pct",
    "ccl4_pct",
    "sf6_pct",
    "region"
FROM "glodap-cruise-uncertainties"
