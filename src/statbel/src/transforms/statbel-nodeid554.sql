-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    CAST("CD_YEAR" AS BIGINT) AS cd_year,
    CAST("CD_MUNTY_REFNIS" AS BIGINT) AS cd_munty_refnis,
    "CD_SECTOR" AS cd_sector,
    CAST("MS_NBR_NON_ZERO_INC" AS BIGINT) AS ms_nbr_non_zero_inc,
    "MS_TOT_NET_TAXABLE_INC" AS ms_tot_net_taxable_inc,
    "MS_AVG_TOT_NET_TAXABLE_INC" AS ms_avg_tot_net_taxable_inc,
    "MS_MEDIAN_NET_TAXABLE_INC" AS ms_median_net_taxable_inc,
    "MS_INT_QUART_DIFF" AS ms_int_quart_diff,
    "MS_INT_QUART_COEFF" AS ms_int_quart_coeff,
    "MS_INT_QUART_ASSYM" AS ms_int_quart_assym,
    "TX_SECTOR_DESCR_NL" AS tx_sector_descr_nl,
    "TX_SECTOR_DESCR_FR" AS tx_sector_descr_fr
FROM "statbel-nodeid554"
