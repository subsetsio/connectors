-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nom_bacia",
    strptime("ena_data", '%Y-%m-%d')::DATE AS ena_data,
    CAST("ena_bruta_bacia_mwmed" AS DOUBLE) AS ena_bruta_bacia_mwmed,
    CAST("ena_bruta_bacia_percentualmlt" AS DOUBLE) AS ena_bruta_bacia_percentualmlt,
    CAST("ena_armazenavel_bacia_mwmed" AS DOUBLE) AS ena_armazenavel_bacia_mwmed,
    CAST("ena_armazenavel_bacia_percentualmlt" AS DOUBLE) AS ena_armazenavel_bacia_percentualmlt
FROM "ons-brazil-ena-diario-por-bacia"
