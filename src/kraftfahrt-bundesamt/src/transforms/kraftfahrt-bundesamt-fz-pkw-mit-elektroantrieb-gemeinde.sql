-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "AGS" AS ags,
    "Gemeinde" AS gemeinde,
    CAST("Berichtszeitpunkt" AS DOUBLE) AS berichtszeitpunkt,
    "Gemeindeschluessel" AS gemeindeschluessel,
    "Stadttyp_Schluessel" AS stadttyp_schluessel,
    "Stadttyp" AS stadttyp,
    "Pkw_insgesamt" AS pkw_insgesamt,
    "ZS_Pkw_insgesamt" AS zs_pkw_insgesamt,
    "Pkw_Elektro" AS pkw_elektro,
    "ZS_Pkw_Elektro" AS zs_pkw_elektro,
    "Pkw_BEV" AS pkw_bev,
    "ZS_Pkw_BEV" AS zs_pkw_bev,
    "Pkw_Plug_In_Hybrid" AS pkw_plug_in_hybrid,
    "ZS_Pkw_Plug_In_Hybrid" AS zs_pkw_plug_in_hybrid,
    "Pkw_Brennstoffzelle" AS pkw_brennstoffzelle,
    "ZS_Pkw_Brennstoffzelle" AS zs_pkw_brennstoffzelle,
    "Pkw_Elektro_Anteil" AS pkw_elektro_anteil,
    "ZS_Pkw_Elektro_Anteil" AS zs_pkw_elektro_anteil,
    "Pkw_BEV_Anteil" AS pkw_bev_anteil,
    "ZS_Pkw_BEV_Anteil" AS zs_pkw_bev_anteil,
    "Pkw_Plug_In_Hybrid_Anteil" AS pkw_plug_in_hybrid_anteil,
    "ZS_Pkw_Plug_In_Hybrid_Anteil" AS zs_pkw_plug_in_hybrid_anteil,
    "Pkw_Brennstoffzelle_Anteil" AS pkw_brennstoffzelle_anteil,
    "ZS_Pkw_Brennstoffzelle_Anteil" AS zs_pkw_brennstoffzelle_anteil,
    "BEZ" AS bez,
    "Shape__Area" AS shape_area,
    "Shape__Length" AS shape_length
FROM "kraftfahrt-bundesamt-fz-pkw-mit-elektroantrieb-gemeinde"
