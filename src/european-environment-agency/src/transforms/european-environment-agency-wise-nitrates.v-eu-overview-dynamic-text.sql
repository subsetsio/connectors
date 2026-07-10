SELECT
    CAST("entry_page_eutro_percentage" AS VARCHAR) AS "entry_page_eutro_percentage",
    CAST("entry_page_GW_percentage" AS VARCHAR) AS "entry_page_GW_percentage",
    CAST("entry_page_NVZ_percentage" AS VARCHAR) AS "entry_page_NVZ_percentage",
    CAST("entry_page_SW_percentage" AS VARCHAR) AS "entry_page_SW_percentage",
    CAST("eutro_page_eutro_percentage" AS VARCHAR) AS "eutro_page_eutro_percentage",
    CAST("eutro_page_lw_percentage" AS VARCHAR) AS "eutro_page_lw_percentage",
    CAST("eutro_page_rw_percentage" AS VARCHAR) AS "eutro_page_rw_percentage",
    CAST("eutro_page_ssw_percentage" AS VARCHAR) AS "eutro_page_ssw_percentage",
    CAST("GW_page_GW_percentage" AS VARCHAR) AS "GW_page_GW_percentage",
    CAST("NVZ_page_NVZ_together_percentage" AS VARCHAR) AS "NVZ_page_NVZ_together_percentage",
    CAST("NVZ_page_share_UAA_percentage" AS VARCHAR) AS "NVZ_page_share_UAA_percentage"
FROM "european-environment-agency-wise-nitrates.v-eu-overview-dynamic-text"
