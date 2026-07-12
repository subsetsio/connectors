-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "400_kv",
    "220_kv",
    "132_kv",
    "66_kv",
    "33_kv",
    "11kv_gm_i_d",
    "11kv_gm_o_d",
    "11kv_pm_pmt"
FROM "qatar-planning-and-statistics-authority-electricity-sub-stations-by-voltage-level"
