-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "id_municipio",
    "id_escola",
    "id_escola_sp",
    "nota_idesp_ef_iniciais",
    "nota_idesp_ef_finais",
    "nota_idesp_em"
FROM "base-dos-dados-br-sp-seduc-idesp--escola"
