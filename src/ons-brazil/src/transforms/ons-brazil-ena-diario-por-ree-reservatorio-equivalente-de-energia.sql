-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The verified row identity includes the measured inflow percentage because the source does not expose a stable observation id.
SELECT
    "nom_reservatorioee",
    strptime("ena_data", '%Y-%m-%d')::DATE AS ena_data,
    CAST("ena_bruta_ree_mwmed" AS DOUBLE) AS ena_bruta_ree_mwmed,
    CAST("ena_bruta_ree_percentualmlt" AS DOUBLE) AS ena_bruta_ree_percentualmlt,
    CAST("ena_armazenavel_ree_mwmed" AS DOUBLE) AS ena_armazenavel_ree_mwmed,
    CAST("ena_armazenavel_ree_percentualmlt" AS DOUBLE) AS ena_armazenavel_ree_percentualmlt
FROM "ons-brazil-ena-diario-por-ree-reservatorio-equivalente-de-energia"
