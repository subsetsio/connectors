-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    "BE" AS be,
    "CD_REG" AS cd_reg,
    "CD_PROV" AS cd_prov,
    CAST("CD_MUNTY_REFNIS" AS BIGINT) AS cd_munty_refnis,
    "TX_MUNTY_DESCR_NL" AS tx_munty_descr_nl,
    "TX_MUNTY_DESCR_FR" AS tx_munty_descr_fr,
    "CD_ISCED_CL" AS cd_isced_cl,
    CAST("MS_POPULATION" AS BIGINT) AS ms_population,
    "MS_POPULATION_25" AS ms_population_25
FROM "statbel-nodeid3453"
