-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ancienne_region",
    "dernier_jour_du_mois",
    "code_ancienne_region",
    "taux_impayes_fin_mois",
    "taux_impayes_fin_mois_suivant",
    "taux_impayes_echeance_90_jours",
    "glissement_trim_tx_fin_mois",
    "glissement_trim_tx_fin_mois_suiv",
    "glissement_trim_tx_90_jours",
    "glissement_annuel_tx_fin_mois",
    "glissement_annu_tx_fin_mois_suiv",
    "glissement_annuel_tx_90_jours"
FROM "urssaf-taux-rar-horsto-mensuels-entreprises-de-10-salaries-ou-plus-par-ancienne-region"
