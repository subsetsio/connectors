-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "freq",
    "ref_area",
    "demand_prod",
    "accounting_entry",
    "counterpart_area",
    "interactors",
    "bridge_items",
    "airpol",
    "sto",
    "unit_measure",
    "product",
    "sector",
    "conf_status",
    "obs_status_1",
    "obs_status_2",
    "obs_status_3",
    "obs_status_4",
    "comment_dset",
    "comment_obs",
    "comment_ts",
    "unit_mult",
    "embargo_time",
    "decimals",
    "title",
    "title_compl",
    "last_update",
    "compiling_org",
    "pre_break_value",
    "diss_org",
    "time_period",
    "value"
FROM "oecd-estat:seea-aea-a"
