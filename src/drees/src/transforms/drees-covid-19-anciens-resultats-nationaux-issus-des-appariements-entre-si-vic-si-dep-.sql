-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "vac_statut",
    "nb_pcr",
    "nb_pcr_sympt",
    "nb_pcr0",
    "nb_pcr_sympt0",
    "hc",
    "hc_pcr",
    "sc",
    "sc_pcr",
    "dc",
    "dc_pcr",
    "effectif_j_7"
FROM "drees-covid-19-anciens-resultats-nationaux-issus-des-appariements-entre-si-vic-si-dep-"
