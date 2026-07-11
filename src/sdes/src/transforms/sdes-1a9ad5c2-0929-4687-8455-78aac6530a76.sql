-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "EPCI_CODE" AS epci_code,
    "EPCI_LIBELLE" AS epci_libelle,
    "INDICATEUR_EXPOSITION" AS indicateur_exposition,
    "VALEUR_EXPOSITION" AS valeur_exposition
FROM "sdes-1a9ad5c2-0929-4687-8455-78aac6530a76"
