-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "Bundesland" AS bundesland,
    CAST("Berichtsjahr" AS BIGINT) AS berichtsjahr,
    "Art_der_Zuwiderhandlung" AS art_der_zuwiderhandlung,
    "Rechtliche_Einordnung" AS rechtliche_einordnung,
    "Lebensalter" AS lebensalter,
    "Anzahl" AS anzahl,
    "ZS_Anzahl" AS zs_anzahl,
    "Anteil_an_Gesamt_je_BL" AS anteil_an_gesamt_je_bl,
    "ZS_Anteil_an_Gesamt_je_BL" AS zs_anteil_an_gesamt_je_bl,
    "Anteil_Owi_Gesamt_je_BL" AS anteil_owi_gesamt_je_bl,
    "ZS_Anteil_Owi_Gesamt_je_BL" AS zs_anteil_owi_gesamt_je_bl,
    "Anteil_Straf_Gesamt_je_BL" AS anteil_straf_gesamt_je_bl,
    "ZS_Anteil_Straf_Gesamt_je_BL" AS zs_anteil_straf_gesamt_je_bl,
    "Anzahl_je_100000_Einwohner" AS anzahl_je_100000_einwohner,
    "ZS_Anzahl_je_100000_Einwohner" AS zs_anzahl_je_100000_einwohner,
    "Veraenderung_VJ" AS veraenderung_vj,
    "ZS_Veraenderung_VJ" AS zs_veraenderung_vj
FROM "kraftfahrt-bundesamt-kf-verkehrsauff-lligkeiten"
