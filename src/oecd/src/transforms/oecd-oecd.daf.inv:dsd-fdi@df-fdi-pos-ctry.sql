-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "unit_measure",
    "measure_principle",
    "accounting_entry",
    "type_entity",
    "fdi_comp",
    "sector",
    "counterpart_area",
    "level_counterpart",
    "activity",
    "freq",
    "fdi_collection_id",
    "obs_status",
    "unit_mult",
    "conf_status",
    "currency",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.daf.inv:dsd-fdi@df-fdi-pos-ctry"
