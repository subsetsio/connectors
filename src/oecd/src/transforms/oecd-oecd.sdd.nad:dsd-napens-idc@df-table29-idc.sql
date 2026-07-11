-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "freq",
    "ref_area",
    "counterpart_area",
    "ref_sector",
    "counterpart_sector",
    "sto",
    "instr_asset",
    "pension_fundtype",
    "accounting_entry",
    "unit_measure",
    "table_identifier",
    "obs_status",
    "conf_status",
    "comment_obs",
    "embargo_date",
    "ref_period_detail",
    "repyearstart",
    "repyearend",
    "time_format",
    "time_per_collect",
    "decimals",
    "title",
    "title_compl",
    "unit_mult",
    "last_update",
    "compiling_org",
    "comment_dset",
    "comment_ts",
    "pre_break_value",
    "data_comp",
    "currency",
    "diss_org",
    "time_period",
    "value"
FROM "oecd-oecd.sdd.nad:dsd-napens-idc@df-table29-idc"
