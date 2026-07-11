-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "patent_authorities",
    "freq",
    "measure",
    "unit_measure",
    "date_type",
    "ref_area",
    "partner_area",
    "agent_role",
    "cooperation_type",
    "wipo",
    "oecd_technology_patent",
    "obs_status",
    "decimals",
    "unit_mult",
    "time_period",
    "value"
FROM "oecd-oecd.sti.pie:dsd-patents@df-patents-oecdspecific"
