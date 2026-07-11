-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FID" AS fid,
    "id_5km",
    "elektro_an",
    "ZS_Anteil_" AS zs_anteil,
    CAST("berichtsj" AS BIGINT) AS berichtsj,
    "Shape__Area" AS shape_area,
    "Shape__Length" AS shape_length
FROM "kraftfahrt-bundesamt-fz-pkw-mit-elektro-antrieb-regionen-gitterzellen-01-01-2025"
