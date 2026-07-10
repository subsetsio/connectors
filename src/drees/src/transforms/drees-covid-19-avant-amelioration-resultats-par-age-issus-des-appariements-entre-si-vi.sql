-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "vac_statut",
    "age",
    "nb_pcr",
    "nb_pcr_sympt",
    "nb_pcr_sympt0",
    "nb_pcr0",
    "hc",
    "hc_pcr",
    "sc",
    "sc_pcr",
    "dc",
    "dc_pcr",
    "effectif",
    "pcr_pourcent_omicron",
    "pcr_sympt_pourcent_omicron",
    "hc_pourcent_omicron",
    "sc_pourcent_omicron",
    "dc_pourcent_omicron",
    "hc_pcr_pour_covid",
    "sc_pcr_pour_covid",
    "dc_pcr_pour_covid"
FROM "drees-covid-19-avant-amelioration-resultats-par-age-issus-des-appariements-entre-si-vi"
