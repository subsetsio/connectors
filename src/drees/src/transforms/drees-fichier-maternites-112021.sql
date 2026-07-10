-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "nom_mat",
    "type",
    "statut",
    "fi_et",
    "fi_ej",
    "com",
    "nomcom",
    "cpo",
    "adresse",
    CAST("lit_obs" AS BIGINT) AS lit_obs,
    CAST("saltrav" AS BIGINT) AS saltrav,
    "acctot"
FROM "drees-fichier-maternites-112021"
