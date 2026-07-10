-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annees",
    "total_ivg_brut",
    "total_ivg_sans_reprises",
    "ratio_d_avortement_brut",
    "ratio_d_avortement_sans_reprises"
FROM "drees-er-ivg-graf1-sept-2024"
