-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Año Fiscal" AS a_o_fiscal,
    "Número de Contrato" AS n_mero_de_contrato,
    "Enm." AS enm,
    "Contratista" AS contratista,
    "Fec. Otorg." AS fec_otorg,
    "Vig. Desde" AS vig_desde,
    "Vig. Hasta" AS vig_hasta,
    "Cuantía" AS cuant_a,
    "Categoría de Servicio" AS categor_a_de_servicio,
    "Tipo de Servicio" AS tipo_de_servicio
FROM "instituto-de-estad-sticas-de-puerto-rico-municipio-de-autonomo-de-caguas-contratos-2013-a-marzo-2018"
