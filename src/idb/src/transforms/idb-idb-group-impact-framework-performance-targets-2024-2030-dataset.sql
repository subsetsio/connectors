-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Numéro_du_Projet" AS num_ro_du_projet,
    "Numéro_de_la_Relation" AS num_ro_de_la_relation,
    "Nom_du_Projet" AS nom_du_projet,
    "Pays" AS pays,
    CAST("Année" AS BIGINT) AS ann_e,
    "Entité" AS entit,
    "Type_d’Opération" AS type_d_op_ration,
    CAST("Montant" AS DOUBLE) AS montant,
    "Petit_pays_vulnérable" AS petit_pays_vuln_rable,
    "source_resource"
FROM "idb-idb-group-impact-framework-performance-targets-2024-2030-dataset"
