-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "champ",
    "annee",
    "sexe",
    "variable",
    "intitule",
    "premier_quintile",
    "deuxieme_quintile",
    "troisieme_quintile",
    "quatrieme_quintile",
    "cinquieme_quintile",
    "ensemble"
FROM "drees-rec06"
