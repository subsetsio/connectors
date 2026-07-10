-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Long-format indicator table mixing summary rows (modalite null) with per-modality rows; filter modalite before aggregating.
SELECT
    "annee",
    "famille_d_organisme",
    "type_de_contrat",
    "theme",
    "type_d_indicateur",
    "indicateur",
    "modalite",
    "valeur",
    "unite"
FROM "drees-enquete-oc-depuis-2019"
