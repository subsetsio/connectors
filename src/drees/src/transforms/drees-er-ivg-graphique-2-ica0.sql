-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annees",
    "ivg_pour_1_000_femmes_tous_ages_en",
    "ivg_pour_1_000_femmes_sans_reprises_en",
    "ica",
    "ica_sans_reprises"
FROM "drees-er-ivg-graphique-2-ica0"
