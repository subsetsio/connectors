-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Vivienda_%_del_gasto_total" AS vivienda_del_gasto_total,
    CAST("None" AS DOUBLE) AS none,
    "source_resource"
FROM "idb-database-of-public-investment-expenditures-in-latin-america-bdd-gipal-2000-"
