-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "freq",
    "territorial_level",
    "ref_area",
    "territorial_type",
    "patent_authorities",
    "date_type",
    "measure",
    "agent_role",
    "oecd_technology_patent",
    "sect_perf",
    "prices",
    "sex",
    "unit_measure",
    "country",
    "obs_status",
    "ref_year_price",
    "unit_mult",
    "decimals",
    "currency",
    "time_period",
    "value"
FROM "oecd-oecd.cfe.eds:dsd-reg-innov@df-rd-gerd"
