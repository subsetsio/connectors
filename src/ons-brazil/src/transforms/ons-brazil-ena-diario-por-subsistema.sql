-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The verified row identity is value-based; filter the region and date fields before using this as a regional time series.
SELECT
    "id_subsistema",
    "nom_subsistema",
    strptime("ena_data", '%Y-%m-%d')::DATE AS ena_data,
    CAST("ena_bruta_regiao_mwmed" AS DOUBLE) AS ena_bruta_regiao_mwmed,
    CAST("ena_bruta_regiao_percentualmlt" AS DOUBLE) AS ena_bruta_regiao_percentualmlt,
    CAST("ena_armazenavel_regiao_mwmed" AS DOUBLE) AS ena_armazenavel_regiao_mwmed,
    CAST("ena_armazenavel_regiao_percentualmlt" AS DOUBLE) AS ena_armazenavel_regiao_percentualmlt
FROM "ons-brazil-ena-diario-por-subsistema"
