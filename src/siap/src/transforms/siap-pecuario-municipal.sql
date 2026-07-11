-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are denormalized observations with geography, species, and product labels repeated on each row; aggregate only after choosing the intended geography and product dimensions.
SELECT
    "source_year",
    "anio",
    CAST("cveestado" AS BIGINT) AS cveestado,
    "nomestado",
    CAST("cveddr" AS BIGINT) AS cveddr,
    "nomddr",
    CAST("cvempio" AS BIGINT) AS cvempio,
    "nommunicipio",
    CAST("cveespecie" AS BIGINT) AS cveespecie,
    "nomespecie",
    CAST("cveproducto" AS BIGINT) AS cveproducto,
    "nomproducto",
    "volumen",
    "peso",
    "precio",
    "valor",
    "asacrificado"
FROM "siap-pecuario-municipal"
