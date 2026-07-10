-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "poste_lib",
    "poste_code",
    "poste_niveau",
    "type",
    "montant"
FROM "drees-comptes-de-la-sante-partage-volume-prix"
