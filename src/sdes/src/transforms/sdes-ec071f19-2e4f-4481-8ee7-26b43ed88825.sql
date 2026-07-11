-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "POLLUANT" AS polluant,
    "CODE_AGGLOMERATION" AS code_agglomeration,
    "NOM_AGGLOMERATION" AS nom_agglomeration,
    "NB_ANNEE_MESURE" AS nb_annee_mesure,
    "NB_ANNEE_DEP" AS nb_annee_dep
FROM "sdes-ec071f19-2e4f-4481-8ee7-26b43ed88825"
