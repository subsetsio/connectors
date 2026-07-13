-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    "service",
    "general_tariff_type",
    CAST("mean_nblocks" AS DOUBLE) AS mean_nblocks,
    CAST("sd_nblocks" AS DOUBLE) AS sd_nblocks,
    CAST("mean_size_1block" AS DOUBLE) AS mean_size_1block,
    CAST("sd_size_1block" AS DOUBLE) AS sd_size_1block,
    CAST("mean_kinkpoint" AS DOUBLE) AS mean_kinkpoint,
    CAST("sd_kinkpoint" AS DOUBLE) AS sd_kinkpoint,
    CAST("mean_price1" AS DOUBLE) AS mean_price1,
    CAST("sd_price1" AS DOUBLE) AS sd_price1,
    CAST("mean_fixedfee1" AS DOUBLE) AS mean_fixedfee1,
    CAST("sd_fixedfee1" AS DOUBLE) AS sd_fixedfee1,
    CAST("mean_pricefinalblock" AS DOUBLE) AS mean_pricefinalblock,
    CAST("sd_pricefinalblock" AS DOUBLE) AS sd_pricefinalblock,
    CAST("mean_mincharged" AS DOUBLE) AS mean_mincharged,
    CAST("sd_mincharge" AS DOUBLE) AS sd_mincharge,
    CAST("mean_1m3" AS DOUBLE) AS mean_1m3,
    CAST("sd_1m3" AS DOUBLE) AS sd_1m3,
    CAST("mean_6m3" AS DOUBLE) AS mean_6m3,
    CAST("sd_6m3" AS DOUBLE) AS sd_6m3,
    CAST("mean_12m3" AS DOUBLE) AS mean_12m3,
    CAST("sd_12m3" AS DOUBLE) AS sd_12m3,
    CAST("mean_15m3" AS DOUBLE) AS mean_15m3,
    CAST("sd_15m3" AS DOUBLE) AS sd_15m3,
    CAST("mean_20m3" AS DOUBLE) AS mean_20m3,
    CAST("sd_20m3" AS DOUBLE) AS sd_20m3,
    CAST("n" AS BIGINT) AS n,
    "subsidy_type",
    "source_resource"
FROM "idb-summary-dataset-water-and-sanitation-tariffs-in-latin-america"
