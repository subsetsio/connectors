-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a frozen historical national-schema series ending in 2005; current livestock observations are published in the municipal-schema table.
SELECT
    "source_year",
    "anio",
    CAST("cveestado" AS BIGINT) AS cveestado,
    "nomestado",
    CAST("cveespecie" AS BIGINT) AS cveespecie,
    "nomespecie",
    CAST("cveproducto" AS BIGINT) AS cveproducto,
    "nomproducto",
    "volumen",
    "peso",
    "precio",
    "valor",
    "asacrificado"
FROM "siap-pecuario-nacional"
