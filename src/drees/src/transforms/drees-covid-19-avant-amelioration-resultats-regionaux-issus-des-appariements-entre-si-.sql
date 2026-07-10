-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "region",
    "vac_statut",
    "nb_pcr",
    "nb_pcr_sympt",
    "nb_pcr0",
    "nb_pcr_sympt0",
    "hc",
    "hc_pcr",
    "sc",
    "sc_pcr",
    "effectif",
    "pcr_pourcent_omicron",
    "pcr_sympt_pourcent_omicron",
    "hc_pourcent_omicron",
    "sc_pourcent_omicron",
    "pcr_pourcent_apparie",
    "hc_pcr_pourcent_apparie"
FROM "drees-covid-19-avant-amelioration-resultats-regionaux-issus-des-appariements-entre-si-"
