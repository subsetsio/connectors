-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Bedrijfsgroepen" AS bedrijfsgroepen,
    "WarmtekrachtkoppelingWKK" AS warmtekrachtkoppelingwkk,
    "TypenInstallatie" AS typeninstallatie,
    "Perioden" AS perioden,
    "InzetTotaal_1" AS inzettotaal_1,
    "InzetVanAardgas_2" AS inzetvanaardgas_2,
    "InzetVanStookolie_3" AS inzetvanstookolie_3,
    "InzetVanSteenkool_4" AS inzetvansteenkool_4,
    "InzetVanOverigeBrandstoffen_5" AS inzetvanoverigebrandstoffen_5,
    "InzetTotaal_6" AS inzettotaal_6,
    "InzetVanAardgas_7" AS inzetvanaardgas_7,
    "InzetVanStookolie_8" AS inzetvanstookolie_8,
    "InzetVanSteenkool_9" AS inzetvansteenkool_9,
    "InzetVanOverigeBrandstoffen_10" AS inzetvanoverigebrandstoffen_10,
    "ProductieTotaal_11" AS productietotaal_11,
    "ProductieVanElektriciteit_12" AS productievanelektriciteit_12,
    "ProductieVanWarmte_13" AS productievanwarmte_13,
    "ProductieTotaal_14" AS productietotaal_14,
    "ProductieVanElektriciteit_15" AS productievanelektriciteit_15,
    "ProductieVanWarmte_16" AS productievanwarmte_16,
    "ElektrischVermogen_17" AS elektrischvermogen_17,
    "ThermischVermogen_18" AS thermischvermogen_18,
    "Installaties_19" AS installaties_19,
    "Bedrijfsgroepen_label" AS bedrijfsgroepen_label,
    "WarmtekrachtkoppelingWKK_label" AS warmtekrachtkoppelingwkk_label,
    "TypenInstallatie_label" AS typeninstallatie_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-37823wkk"
