-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Fecha de publicación (en o antes)" AS fecha_de_publicaci_n_en_o_antes,
    "Título del informe" AS t_tulo_del_informe,
    "Fuente" AS fuente,
    "Periodo de referencia" AS periodo_de_referencia
FROM "instituto-de-estad-sticas-de-puerto-rico-calendario"
