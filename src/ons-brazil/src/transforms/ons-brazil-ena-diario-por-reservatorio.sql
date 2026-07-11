-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nom_reservatorio",
    "cod_resplanejamento",
    "tip_reservatorio",
    "nom_bacia",
    "nom_ree",
    "id_subsistema",
    "nom_subsistema",
    strptime("ena_data", '%Y-%m-%d')::DATE AS ena_data,
    "ena_bruta_res_mwmed",
    "ena_bruta_res_percentualmlt",
    "ena_armazenavel_res_mwmed",
    "ena_armazenavel_res_percentualmlt",
    "ena_queda_bruta",
    "mlt_ena"
FROM "ons-brazil-ena-diario-por-reservatorio"
