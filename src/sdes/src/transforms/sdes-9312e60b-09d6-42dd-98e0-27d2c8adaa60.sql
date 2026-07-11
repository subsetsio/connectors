-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "EPCI_CODE" AS epci_code,
    "EPCI_LIBELLE" AS epci_libelle,
    "PERIODE_CONSTRUCTION" AS periode_construction,
    "LOGEMENTS_EXPOSES" AS logements_exposes
FROM "sdes-9312e60b-09d6-42dd-98e0-27d2c8adaa60"
