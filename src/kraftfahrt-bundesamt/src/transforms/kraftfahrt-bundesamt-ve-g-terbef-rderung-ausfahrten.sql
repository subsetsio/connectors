-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fid",
    CAST("Jahr" AS BIGINT) AS jahr,
    "Hauptverkehrsbeziehung" AS hauptverkehrsbeziehung,
    "Beheimatung" AS beheimatung,
    "Beladeregion" AS beladeregion,
    "Beladeregion_Klartext" AS beladeregion_klartext,
    "Entladeregion" AS entladeregion,
    "Entladeregion_Klartext" AS entladeregion_klartext,
    "Gueterpositionen_7_Klartext" AS gueterpositionen_7_klartext,
    "Fahrten" AS fahrten,
    "ZS_Fahrten" AS zs_fahrten,
    "Kilometer" AS kilometer,
    "ZS_Kilometer" AS zs_kilometer,
    "Tonnen" AS tonnen,
    "ZS_Tonnen" AS zs_tonnen,
    "Tkm" AS tkm,
    "ZS_Tkm" AS zs_tkm,
    "Fahrzeugdatensaetze" AS fahrzeugdatensaetze,
    "Shape__Area" AS shape_area,
    "Shape__Length" AS shape_length
FROM "kraftfahrt-bundesamt-ve-g-terbef-rderung-ausfahrten"
