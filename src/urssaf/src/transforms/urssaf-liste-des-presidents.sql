-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "libelle_organisme",
    "libelle_site",
    "code_site_v2",
    "code_organisme_ur_regionale",
    "code_rap_organisme",
    "identifiant_site_rioss",
    "siege_social",
    "adresse",
    "code_postal",
    "ville",
    "pays",
    "prenom_president_regional",
    "nom_president_regional",
    "annee_arrivee",
    "annee_depart"
FROM "urssaf-liste-des-presidents"
