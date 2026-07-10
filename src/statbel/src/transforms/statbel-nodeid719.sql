-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    "CD_PRODCOM_2016" AS cd_prodcom_2016,
    "TX_PRODCOM_FR" AS tx_prodcom_fr,
    "TX_PRODCOM_NL" AS tx_prodcom_nl,
    "CD_UNIT" AS cd_unit,
    "CD_TYPE" AS cd_type
FROM "statbel-nodeid719"
