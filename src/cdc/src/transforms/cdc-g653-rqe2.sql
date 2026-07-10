-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "key_plot_id",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    CAST("pcr_conc_lin" AS DOUBLE) AS pcr_conc_lin,
    "normalization"
FROM "cdc-g653-rqe2"
