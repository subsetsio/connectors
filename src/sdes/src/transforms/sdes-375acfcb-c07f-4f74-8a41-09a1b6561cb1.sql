-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "POLLUANT" AS polluant,
    "ANNEE" AS annee,
    "CODE_AGGLOMERATION" AS code_agglomeration,
    "NOM_AGGLOMERATION" AS nom_agglomeration,
    "SITUATION_REGLEMENTATION" AS situation_reglementation
FROM "sdes-375acfcb-c07f-4f74-8a41-09a1b6561cb1"
