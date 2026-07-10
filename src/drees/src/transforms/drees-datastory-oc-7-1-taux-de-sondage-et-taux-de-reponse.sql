-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Includes an all-organismes total row with a null grouping dimension; keyless — filter it out before aggregating across familles_d_organismes.
SELECT
    "familles_d_organismes",
    CAST("annee" AS BIGINT) AS annee,
    "taille_de_la_population_totale_organismes",
    "champ_de_l_enquete",
    "taille_de_l_echantillon",
    "nombre_de_repondants",
    "montant_des_cotisations_de_la_population_millions_eur",
    "montant_des_cotisations_de_l_echantillon_millions_eur",
    "montant_des_cotisations_des_repondants_millions_eur",
    "taux_de_sondage_en",
    "taux_de_sondage_des_cotisations_en",
    "taux_de_reponse_en",
    "taux_de_reponse_des_cotisations_en"
FROM "drees-datastory-oc-7-1-taux-de-sondage-et-taux-de-reponse"
