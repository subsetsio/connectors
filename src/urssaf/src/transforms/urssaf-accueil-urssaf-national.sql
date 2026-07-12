-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "code_commune_insee",
    "nom_commune",
    "region",
    "organisme",
    "site",
    "titre_du_site",
    "adresse",
    "date_mise_a_jour",
    "accueil_sans_rendez_vous",
    "jours_d_accueil_sans_rendez_vous",
    "horaires_d_accueil_sans_rendez_vous",
    "nbre_demi_journees_ouverture_public",
    "accueil_sur_rendez_vous",
    "jour_d_accueil_sur_rendez_vous",
    "horaires_d_accueil_sur_rendez_vous",
    "nbre_demi_journees_accueil_sur_rdv",
    "rdv_physiques",
    "rdv_telephoniques",
    "rdv_visio",
    "accueil_commun_ti",
    "bornes_disponibles",
    "espace_demarche_en_ligne",
    "paiement_par_carte_bancaire",
    "centroid"
FROM "urssaf-accueil-urssaf-national"
