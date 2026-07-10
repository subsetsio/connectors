-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    CAST("cd_year" AS BIGINT) AS cd_year,
    CAST("cd_refnis" AS BIGINT) AS cd_refnis,
    "tx_descr_fr",
    "tx_descr_nl",
    "tx_descr_de",
    "tx_descr_en",
    "tx_hh_type_fr",
    "tx_hh_type_nl",
    "tx_hh_type_de",
    "tx_hh_type_en",
    "cd_cars_per_hh",
    CAST("ms_num_hh" AS BIGINT) AS ms_num_hh,
    CAST("ms_num_car" AS BIGINT) AS ms_num_car
FROM "statbel-nodeid4759"
