-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "sigla_uf",
    "rede",
    "diretoria",
    "id_municipio",
    "id_escola",
    "id_escola_sp",
    "codigo_tipo_escola",
    "prop_aprovados_anos_inciais_ef",
    "prop_reprovados_anos_iniciais_ef",
    "prop_abandono_anos_iniciais_ef",
    "prop_aprovados_anos_finais_ef",
    "prop_reprovados_anos_finais_ef",
    "prop_abandono_anos_finais_ef",
    "prop_aprovados_em",
    "prop_reprovados_em",
    "prop_abandono_em"
FROM "base-dos-dados-br-sp-seduc-fluxo-escolar--escola"
