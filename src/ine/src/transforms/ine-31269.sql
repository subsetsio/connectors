-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row is one INE time-series observation for a source series; totals, subtotals, rates, indexes, coefficients, and counts can coexist as separate series within the same source table.
-- caution: Use serie_cod or serie_nombre to isolate a statistical series before aggregating valor across dates or categories.
SELECT
    CAST("table_id" AS BIGINT) AS table_id,
    "serie_cod",
    "serie_nombre",
    "fk_unidad",
    "fk_escala",
    "fecha_ms",
    "fecha",
    "anyo",
    "fk_periodo",
    "fk_tipodato",
    "valor",
    "secreto"
FROM "ine-31269"
