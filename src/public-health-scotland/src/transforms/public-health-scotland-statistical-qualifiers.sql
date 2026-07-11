-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Reference-style source extract without a verified compact key; use the source columns as descriptive records rather than aggregating rows.
SELECT
    "resource_id",
    "resource_name",
    "Qualifier" AS qualifier,
    "QualifierName" AS qualifiername,
    "QualifierDefinition" AS qualifierdefinition
FROM "public-health-scotland-statistical-qualifiers"
