-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "geo",
    "pays",
    "annee",
    "code",
    "depense",
    "valeur",
    "moy11",
    "ecart"
FROM "drees-skyline"
