-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows span three nested levels of the fee-type hierarchy; `honoraires_ordre_niv_2`/`_3` carry the sentinel 99 (and their `type_honoraires_niveau_2`/`_3` labels are null) on rows that stop at a shallower level. Summing `montant_honoraires` across levels double-counts.
-- caution: Aggregate members also exist in `profession_sante` and the territory columns; `montant_honoraires_moyens` is a per-practitioner mean and is never summable.
SELECT
    "annee",
    "profession_sante",
    "region",
    "libelle_region",
    "departement",
    "libelle_departement",
    "honoraires_ordre_niv_1",
    "type_honoraires_niveau_1",
    "honoraires_ordre_niv_2",
    "type_honoraires_niveau_2",
    "honoraires_ordre_niv_3",
    "type_honoraires_niveau_3",
    "montant_honoraires",
    "montant_honoraires_moyens",
    "vision_generale_all",
    "vision_profession_territoire",
    "vision_honoraires_actes_niveau_2",
    "vision_honoraires_remunerations_niveau_2",
    "vision_honoraires_actescliniques_niveau_3",
    "vision_honoraires_actestechniques_niveau_3"
FROM "cnam-honoraires-detailles"
