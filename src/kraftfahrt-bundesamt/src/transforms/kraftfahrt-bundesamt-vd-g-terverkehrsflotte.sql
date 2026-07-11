-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "REGION_LAB" AS region_lab,
    CAST("Jahr" AS BIGINT) AS jahr,
    "Monat" AS monat,
    "Monat_Text" AS monat_text,
    "ZS_Anteil_Zeile_Gesamt_Ins" AS zs_anteil_zeile_gesamt_ins,
    "Anteil_Zeile_Gesamt_Ins" AS anteil_zeile_gesamt_ins,
    "ZS_Anteil_Zeile_Gesamt_Lkw" AS zs_anteil_zeile_gesamt_lkw,
    "Anteil_Zeile_Gesamt_Lkw" AS anteil_zeile_gesamt_lkw,
    "ZS_Anteil_Zeile_Gesamt_Sat" AS zs_anteil_zeile_gesamt_sat,
    "Anteil_Zeile_Gesamt_Sat" AS anteil_zeile_gesamt_sat,
    "ZS_Anteil_Zeile_Region_Ins" AS zs_anteil_zeile_region_ins,
    "Anteil_Zeile_Region_Ins" AS anteil_zeile_region_ins,
    "ZS_Anteil_Zeile_Region_Lkw" AS zs_anteil_zeile_region_lkw,
    "Anteil_Zeile_Region_Lkw" AS anteil_zeile_region_lkw,
    "ZS_Anteil_Zeile_Region_Sat" AS zs_anteil_zeile_region_sat,
    "Anteil_Zeile_Region_Sat" AS anteil_zeile_region_sat,
    "ZS_Anz_Ins" AS zs_anz_ins,
    "Anz_Ins" AS anz_ins,
    "ZS_Anz_Lkw" AS zs_anz_lkw,
    "Anz_Lkw" AS anz_lkw,
    "ZS_Anz_Sat" AS zs_anz_sat,
    "Anz_Sat" AS anz_sat,
    "Shape__Area" AS shape_area,
    "Shape__Length" AS shape_length
FROM "kraftfahrt-bundesamt-vd-g-terverkehrsflotte"
