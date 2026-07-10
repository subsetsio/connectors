-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "diretoria",
    "id_diretoria",
    "nota_idesp_ef_iniciais",
    "nota_idesp_ef_finais",
    "nota_idesp_em"
FROM "base-dos-dados-br-sp-seduc-idesp--diretoria"
