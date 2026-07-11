-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "EPCI_CODE" AS epci_code,
    "EPCI_LIBELLE" AS epci_libelle,
    "PERIODE_CONSTRUCTION" AS periode_construction,
    "MAISONS_INDIV_EXPOSES_RGA1" AS maisons_indiv_exposes_rga1,
    "MAISONS_INDIV_EXPOSES_RGA2" AS maisons_indiv_exposes_rga2,
    "MAISONS_INDIV_EXPOSES_RGA3" AS maisons_indiv_exposes_rga3
FROM "sdes-1d6ff531-fe68-4102-9591-8da9ffdf8300"
