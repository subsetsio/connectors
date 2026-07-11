-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    CAST("col_0" AS BIGINT) AS col_0,
    "Organización" AS organizaci_n,
    "Número.de.exención" AS n_mero_de_exenci_n,
    strptime("Fecha.de.efectividad", '%Y-%m-%d')::DATE AS fecha_de_efectividad
FROM "instituto-de-estad-sticas-de-puerto-rico-organizaciones-sin-fines-de-lucro-con-exenciones-otorgadas-por-hacienda"
