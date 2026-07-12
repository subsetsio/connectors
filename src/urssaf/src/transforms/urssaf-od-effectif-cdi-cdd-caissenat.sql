-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "organisme",
    "date_dernier_jour_du_mois",
    "nature_du_contrat",
    "sexe",
    CAST("code_region" AS BIGINT) AS code_region,
    "region",
    "effectif_organisme",
    "geom",
    "centroid"
FROM "urssaf-od-effectif-cdi-cdd-caissenat"
