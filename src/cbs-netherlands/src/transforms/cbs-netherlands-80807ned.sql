-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Bedrijfstypen" AS bedrijfstypen,
    "RegioS" AS regios,
    "Perioden" AS perioden,
    "TotaalAantalLandbouwbedrijven_1" AS totaalaantallandbouwbedrijven_1,
    "VerkoopAanHuisTotaal_2" AS verkoopaanhuistotaal_2,
    "RechtstreekseVerkoopAanDeConsument_3" AS rechtstreekseverkoopaandeconsument_3,
    "VerkoopVia1Tussenschakel_4" AS verkoopvia1tussenschakel_4,
    "StallingVanGoederenOfDieren_5" AS stallingvangoederenofdieren_5,
    "Agrotoerisme_6" AS agrotoerisme_6,
    "VerwerkingLandbouwproducten_7" AS verwerkinglandbouwproducten_7,
    "Zorglandbouw_8" AS zorglandbouw_8,
    "Aquacultuur_9" AS aquacultuur_9,
    "LoonwerkVoorDerden_10" AS loonwerkvoorderden_10,
    "AgrarischNatuurEnLandschapsbeheer_11" AS agrarischnatuurenlandschapsbeheer_11,
    "AgrarischeKinderopvang_12" AS agrarischekinderopvang_12,
    "BoerderijEducatie_13" AS boerderijeducatie_13,
    "EnergieproductieLeveringAanDerden_14" AS energieproductieleveringaanderden_14,
    "OpbrengstMinderDan10_15" AS opbrengstminderdan10_15,
    "Opbrengst1050_16" AS opbrengst1050_16,
    "OpbrengstMeerDan50_17" AS opbrengstmeerdan50_17,
    "Bedrijfstypen_label" AS bedrijfstypen_label,
    "RegioS_label" AS regios_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80807ned"
