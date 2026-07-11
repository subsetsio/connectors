-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The verified row identity includes storage values because the source does not expose a stable equivalent-reservoir observation id.
SELECT
    "nom_ree",
    strptime("ear_data", '%Y-%m-%d')::DATE AS ear_data,
    CAST("ear_max_ree" AS DOUBLE) AS ear_max_ree,
    CAST("ear_verif_ree_mwmes" AS DOUBLE) AS ear_verif_ree_mwmes,
    CAST("ear_verif_ree_percentual" AS DOUBLE) AS ear_verif_ree_percentual
FROM "ons-brazil-ear-diario-por-ree-reservatorio-equivalente-de-energia"
