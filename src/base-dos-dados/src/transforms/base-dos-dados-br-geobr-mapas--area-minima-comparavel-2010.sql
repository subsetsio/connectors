-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_amc",
    "id_municipio",
    "geometria"
FROM "base-dos-dados-br-geobr-mapas--area-minima-comparavel-2010"
