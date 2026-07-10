-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    CAST("CD_REFNIS" AS BIGINT) AS cd_refnis,
    "TX_REFNIS_DESCR_NL" AS tx_refnis_descr_nl,
    "TX_REFNIS_DESCR_FR" AS tx_refnis_descr_fr,
    "TX_REFNIS_DESCR_DE" AS tx_refnis_descr_de,
    CAST("CD_ZIP" AS BIGINT) AS cd_zip,
    CAST("CD_STR" AS BIGINT) AS cd_str,
    "TX_STR_NM_NL" AS tx_str_nm_nl,
    "TX_STR_NM_FR" AS tx_str_nm_fr,
    "TX_STR_NM_DE" AS tx_str_nm_de,
    "TX_HO_NR" AS tx_ho_nr,
    "FL_EVEN" AS fl_even,
    "CD_SECTOR_2024" AS cd_sector_2024,
    CAST("XY_X_LB72" AS DOUBLE) AS xy_x_lb72,
    CAST("XY_Y_LB72" AS DOUBLE) AS xy_y_lb72,
    "XY_X_3035" AS xy_x_3035,
    "XY_Y_3035" AS xy_y_3035,
    "XY_X_3812" AS xy_x_3812,
    "XY_Y_3812" AS xy_y_3812,
    "XY_LON_WGS84" AS xy_lon_wgs84,
    "XY_LAT_WGS84" AS xy_lat_wgs84,
    "GRD_NEWID" AS grd_newid,
    "XY_X_LB72_1" AS xy_x_lb72_1,
    "XY_Y_LB72_1" AS xy_y_lb72_1
FROM "statbel-nodeid6300"
