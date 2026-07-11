-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    CAST("Edad" AS BIGINT) AS edad,
    "Sexo" AS sexo,
    "Region" AS region
FROM "instituto-de-estad-sticas-de-puerto-rico-casos-unicos-positivos-por-pruebas-moleculares-covid-19-puerto-rico"
