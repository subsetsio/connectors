-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "phenophase_id",
    "phenophase_name",
    "phenophase_category",
    "color",
    "pheno_class_id"
FROM "usa-npn-phenophases"
