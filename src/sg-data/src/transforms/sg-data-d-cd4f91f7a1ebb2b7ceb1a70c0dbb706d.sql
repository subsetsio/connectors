-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "ura_planning_region",
    "residential_status",
    "num_solar_pv_inst",
    "inst_cap_kwac",
    "total_inst_cap_percent"
FROM "sg-data-d-cd4f91f7a1ebb2b7ceb1a70c0dbb706d"
