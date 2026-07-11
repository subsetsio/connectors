-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nomecurto",
    strptime("ear_data", '%Y-%m-%d')::DATE AS ear_data,
    "ear_max_bacia",
    "ear_verif_bacia_mwmes",
    "ear_verif_bacia_percentual"
FROM "ons-brazil-ear-diario-por-bacia"
