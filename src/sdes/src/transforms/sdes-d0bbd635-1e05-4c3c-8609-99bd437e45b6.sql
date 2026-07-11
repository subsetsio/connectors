-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SUBSTANCE" AS substance,
    "CODE_NACE_REV2_ET_MENAGES" AS code_nace_rev2_et_menages,
    "MASSE" AS masse,
    "ANNEE" AS annee,
    "LIBELLE_NACE_ET_MENAGES" AS libelle_nace_et_menages,
    "LIBELLE_SUBSTANCE" AS libelle_substance
FROM "sdes-d0bbd635-1e05-4c3c-8609-99bd437e45b6"
