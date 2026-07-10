-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Geographic columns include commune-level observations identified with their parent department and region; aggregate carefully by one geographic level at a time.
SELECT
    "date",
    "code_region",
    "region",
    "code_departement",
    "departement",
    "code_commune",
    "commune",
    "type_de_donnees",
    "categorie",
    "sexe",
    "tranche_d_age",
    "nombre_de_demandeurs_d_emploi"
FROM "dares-dares-defm-communales-brutes"
