-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "lib_reg",
    "code_reg",
    "lib_dep",
    "code_dep",
    "thematique",
    "sous_thematique",
    "libelle_indicateur",
    "id_indicateur",
    "value",
    "code_vilas",
    "code_isd",
    "code_tableau_panorama",
    "source",
    "libelle_isd"
FROM "drees-631-insertion-sociale-et-minima-sociaux"
