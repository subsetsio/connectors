-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nature_du_marche",
    "objet_du_marche",
    "montant_ht_estimatif",
    "duree_en_mois",
    "date_de_notification",
    "date_de_fin",
    "titulaire",
    "date_de_notification_unix"
FROM "urssaf-marches-notifies-par-acoss-urssaf-caisse-nationale"
