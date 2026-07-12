-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "libelle_court_fiche_cog",
    "libelle_long_fiche_cog",
    "indicateurs",
    "format_resultat",
    "resultats",
    "etat_indicateur"
FROM "urssaf-urssaf-indicateurs-cog"
