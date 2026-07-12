-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_mention",
    "type_publication",
    "url_publication",
    "mois_publication",
    "annee_publication",
    "date_derniere_consultation",
    "contenu_actif"
FROM "urssaf-mentions-reutilisations-donnees-urssaf"
