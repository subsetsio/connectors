-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "type_de_donnees",
    "libelle",
    "valeur"
FROM "dares-dares-defm-entrees-stages-formation-trim"
