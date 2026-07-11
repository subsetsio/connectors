-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "POLLUANT" AS polluant,
    "POURC_AGGLOMERATIONS" AS pourc_agglomerations
FROM "sdes-a956734e-0f63-4629-821e-669f477d5f53"
