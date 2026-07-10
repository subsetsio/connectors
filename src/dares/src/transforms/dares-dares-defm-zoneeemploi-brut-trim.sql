-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "code_region",
    "region",
    "code_zone_d_emploi",
    "zone_d_emploi",
    "type_de_donnees",
    "categorie",
    "sexe",
    "tranche_d_age",
    "anciennete",
    CAST("nombre_de_demandeurs_d_emploi" AS BIGINT) AS nombre_de_demandeurs_d_emploi
FROM "dares-dares-defm-zoneeemploi-brut-trim"
