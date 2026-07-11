-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ICO" AS ico,
    "OKRESLAU" AS okreslau,
    strptime("DDATVZN", '%Y-%m-%d')::DATE AS ddatvzn,
    strptime("DDATZAN", '%Y-%m-%d')::DATE AS ddatzan,
    "ZPZAN" AS zpzan,
    strptime("DDATPAKT", '%Y-%m-%d')::DATE AS ddatpakt,
    CAST("FORMA" AS BIGINT) AS forma,
    CAST("ROSFORMA" AS BIGINT) AS rosforma,
    "KATPO" AS katpo,
    "NACE" AS nace,
    "NACE2025" AS nace2025,
    CAST("ICZUJ" AS BIGINT) AS iczuj,
    "FIRMA" AS firma,
    CAST("CISS2010" AS BIGINT) AS ciss2010,
    CAST("KODADM" AS BIGINT) AS kodadm,
    "TEXTADR" AS textadr,
    CAST("PSC" AS BIGINT) AS psc,
    "OBEC_TEXT" AS obec_text,
    "COBCE_TEXT" AS cobce_text,
    "ULICE_TEXT" AS ulice_text,
    CAST("TYPCDOM" AS BIGINT) AS typcdom,
    CAST("CDOM" AS BIGINT) AS cdom,
    "COR" AS cor,
    strptime("DATPLAT", '%Y-%m-%d')::DATE AS datplat,
    "PRIZNAK" AS priznak
FROM "czech-statistical-office-res-data"
