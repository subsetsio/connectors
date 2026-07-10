-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix geographic scopes through department and region fields; filter to the intended geography before summing.
SELECT
    "date",
    "code_region",
    "region",
    "code_departement",
    "departement",
    "type_de_donnees",
    "type_d_offre_d_emploi",
    "type_d_emploi",
    "qualification",
    "nombre_d_offres_d_emploi"
FROM "dares-dares-offres-collectees-satisfaites-france-travail-brutes-trim"
