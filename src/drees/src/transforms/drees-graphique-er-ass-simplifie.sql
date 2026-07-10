-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dixieme_de_niveau_de_vie",
    "de_l_ass",
    "de_l_are",
    "du_rsa",
    "ensemble_de_la_population"
FROM "drees-graphique-er-ass-simplifie"
