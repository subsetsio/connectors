-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "vac_statut",
    "age",
    "nb_pcr",
    "nb_pcr0",
    "hc",
    "hc_pcr",
    "sc",
    "sc_pcr",
    "effectif_j_7"
FROM "drees-covid-19-anciens-resultats-par-age-issus-des-appariements-entre-si-vic-si-dep-et"
