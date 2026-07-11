-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DECHET" AS dechet,
    "ANNEE" AS annee,
    "DANGEREUX" AS dangereux,
    "MATIERE_SECHE" AS matiere_seche,
    "VALORISATION" AS valorisation,
    "INCINERATION" AS incineration,
    "RECYCLAGE" AS recyclage,
    "REMBLAYAGE" AS remblayage,
    "DECHARGE" AS decharge,
    "AUTRE_ELIMINATION" AS autre_elimination,
    "TOTAL" AS total
FROM "sdes-fda380ad-4bf0-4fae-bddb-6671deeb610b"
