-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "EPCI_CODE" AS epci_code,
    "EPCI_LIBELLE" AS epci_libelle,
    "INDICATEUR_EXPOSITION" AS indicateur_exposition,
    "VALEUR_EXPOSITION" AS valeur_exposition
FROM "sdes-63c3cde7-ae7e-4985-9e80-44f591ed2047"
