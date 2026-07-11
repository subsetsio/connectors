-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("OBVOD" AS BIGINT) AS obvod,
    "NAZEV_OBV" AS nazev_obv,
    CAST("OKRES" AS BIGINT) AS okres,
    CAST("PRVNI_VO" AS BIGINT) AS prvni_vo,
    "PLATNOST" AS platnost
FROM "czech-statistical-office-se2022secobv"
