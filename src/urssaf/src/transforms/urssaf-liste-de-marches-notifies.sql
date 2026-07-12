-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "nature_du_marche",
    "objet_du_marche",
    "montant_ht_estimatif",
    "duree_en_mois",
    "date_de_notification",
    "date_de_fin",
    "titulaire"
FROM "urssaf-liste-de-marches-notifies"
