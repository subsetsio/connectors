-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period_commissioned",
    "lftr",
    "400_kv",
    "220_kv",
    "132_kv",
    "66_kv",
    "33_kv",
    "11_kv"
FROM "qatar-planning-and-statistics-authority-electricity-cables-laid-by-voltage-level-rkm"
