-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "organisme",
    "dernier_jour_du_mois",
    "nature_de_contrat",
    "libelle_famille_professionnelle",
    "libelle_metier",
    "effectif_organisme"
FROM "urssaf-urssaf-effectif-par-metier"
