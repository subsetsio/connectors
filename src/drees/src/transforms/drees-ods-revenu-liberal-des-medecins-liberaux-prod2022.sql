-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "specialites_medicales",
    "secteur_de_conventionnement",
    "type_de_revenu",
    "revenu_annuel_moyen_en_euros_courants",
    "taux_de_croissance_annuel_moyen_2017_2021_en_en_euros_constants"
FROM "drees-ods-revenu-liberal-des-medecins-liberaux-prod2022"
