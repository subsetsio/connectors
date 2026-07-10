-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("DAY" AS BIGINT) AS day,
    CAST("MONTH" AS BIGINT) AS month,
    CAST("BELGIUM" AS BIGINT) AS belgium,
    CAST("VLAANDEREN" AS BIGINT) AS vlaanderen,
    CAST("WALLONIE" AS BIGINT) AS wallonie,
    CAST("BRUSSELS" AS BIGINT) AS brussels,
    CAST("PROVINCIE_ANTWERPEN" AS BIGINT) AS provincie_antwerpen,
    CAST("PROVINCIE_VLAAMS_BRABANT" AS BIGINT) AS provincie_vlaams_brabant,
    CAST("PROVINCE_BRABANT_WALLON" AS BIGINT) AS province_brabant_wallon,
    CAST("PROVINCIE_WEST_VLAANDEREN" AS BIGINT) AS provincie_west_vlaanderen,
    CAST("PROVINCIE_OOST_VLAANDEREN" AS BIGINT) AS provincie_oost_vlaanderen,
    CAST("PROVINCE_HAINAUT" AS BIGINT) AS province_hainaut,
    CAST("PROVINCE_LIEGE" AS BIGINT) AS province_liege,
    CAST("PROVINCIE_LIMBURG" AS BIGINT) AS provincie_limburg,
    CAST("PROVINCE_LUXEMBOURG" AS BIGINT) AS province_luxembourg,
    CAST("PROVINCE_NAMUR" AS BIGINT) AS province_namur
FROM "statbel-nodeid2587"
