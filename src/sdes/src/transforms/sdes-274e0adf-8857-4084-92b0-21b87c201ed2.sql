-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "EPCI_CODE" AS epci_code,
    "EPCI_LIBELLE" AS epci_libelle,
    "PERIODE_CONSTRUCTION" AS periode_construction,
    "LOGEMENTS_EXPOSES" AS logements_exposes
FROM "sdes-274e0adf-8857-4084-92b0-21b87c201ed2"
