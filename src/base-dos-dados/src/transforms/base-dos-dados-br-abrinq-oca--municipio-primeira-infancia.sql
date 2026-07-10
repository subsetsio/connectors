-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "id_municipio",
    "taxa_bruta_matricula_pre_escola",
    "numero_absoluto_bruto_matricula_pre_escola",
    "taxa_liquida_matricula_pre_escola",
    "numero_absoluto_liquido_matricula_pre_escola"
FROM "base-dos-dados-br-abrinq-oca--municipio-primeira-infancia"
