-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dixieme_de_niveau_de_vie",
    "hommes_population_entiere",
    "hommes_population_nee_en_france",
    "femmes_population_entiere",
    "femmes_population_nee_en_france"
FROM "drees-graphique-er-suicide-complet"
