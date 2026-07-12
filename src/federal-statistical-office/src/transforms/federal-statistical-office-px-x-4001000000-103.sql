-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("jahr" AS BIGINT) AS jahr,
    "kanton_bezirk_gemeinde",
    "haushaltstyp",
    "anzahl_ledige_kinder_unter_18_jahren",
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-4001000000-103"
