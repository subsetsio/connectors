-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "code",
    "libelle",
    "libelle_court",
    "format",
    "taux_plafonne",
    "taux_deplafonne",
    "taux_at",
    "date_d_effet",
    "date_de_fin",
    "specificite"
FROM "urssaf-histocodestypescsv"
