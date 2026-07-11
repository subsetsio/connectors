-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "the_geom",
    "Nombre" AS nombre,
    "Codigo" AS codigo,
    "Rumbo" AS rumbo
FROM "instituto-de-estad-sticas-de-puerto-rico-mapa-de-rutas-de-porteadores-publicos"
