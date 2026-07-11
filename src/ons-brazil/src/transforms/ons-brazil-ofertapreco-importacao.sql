-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nom_pais",
    "nom_agente",
    "nom_bloco",
    strptime("dat_iniciovalidade", '%Y-%m-%d')::DATE AS dat_iniciovalidade,
    strptime("dat_fimvalidade", '%Y-%m-%d')::DATE AS dat_fimvalidade,
    "val_preco"
FROM "ons-brazil-ofertapreco-importacao"
