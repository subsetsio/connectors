-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "grupcnae20",
    CAST("zero" AS BIGINT) AS zero,
    CAST("ate4" AS BIGINT) AS ate4,
    CAST("de5a9" AS BIGINT) AS de5a9,
    CAST("de10a19" AS BIGINT) AS de10a19,
    CAST("de20a49" AS BIGINT) AS de20a49,
    CAST("de50a99" AS BIGINT) AS de50a99,
    CAST("de100a249" AS BIGINT) AS de100a249,
    CAST("de250a499" AS BIGINT) AS de250a499,
    CAST("de500a999" AS BIGINT) AS de500a999,
    CAST("oumais" AS BIGINT) AS oumais,
    CAST("ignorado" AS BIGINT) AS ignorado,
    CAST("total" AS BIGINT) AS total,
    CAST("year" AS BIGINT) AS year,
    "source_resource"
FROM "idb-rais-industry-level-data-associated-with-access-to-credit-and-the-size-of-t"
