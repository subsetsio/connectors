-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "counterpart_area",
    "freq",
    "measure",
    "unit_measure",
    "statistical_operation",
    "aggregation_type",
    "profit_grouping",
    "effective_tax_rate",
    "mne_size",
    "decimals",
    "obs_status",
    "time_period",
    "value"
FROM "oecd-oecd.ctp.tps:dsd-cbcr@df-cbcri"
