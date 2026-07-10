-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dixieme_de_niveau_de_vie",
    "depistage_organise",
    "depistage_individuel",
    "depistage_organise_ou_individuel"
FROM "drees-graphique-er-depistage-cancer0"
