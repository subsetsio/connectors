-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("date_d_observation", '%d/%m/%Y')::DATE AS date_d_observation,
    "mois_d_observation",
    "mois_d_echeance",
    "jour_d_echeance",
    strptime("echeance_de_paiement", '%d/%m/%Y')::DATE AS echeance_de_paiement,
    "code_region",
    "region",
    "code_ancienne_region",
    "ancienne_region",
    "code_departement",
    "departement",
    "grand_secteur_d_activite",
    "nb_etab_a_echeance",
    "cotisations_dues",
    "nb_etab_avec_report",
    "montant_reports",
    "date_num_echeance",
    "date_num_observation",
    "geo_point_2d"
FROM "urssaf-mesures-exceptionnelles-covid-19-reports-par-departement-x-grand-secteur"
