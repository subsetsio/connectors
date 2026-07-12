-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "code_commune",
    "nom_commune",
    "region",
    strptime("date_debut", '%Y%m%d')::DATE AS date_debut,
    strptime("date_fin", '%Y%m%d')::DATE AS date_fin,
    "taux_vm",
    "taux_vma",
    "taux_vmr",
    CAST("code_partenaire_vm" AS BIGINT) AS code_partenaire_vm,
    CAST("code_partenaire_vma" AS BIGINT) AS code_partenaire_vma,
    CAST("code_partenaire_vmr" AS BIGINT) AS code_partenaire_vmr
FROM "urssaf-table-taux-vmrr"
