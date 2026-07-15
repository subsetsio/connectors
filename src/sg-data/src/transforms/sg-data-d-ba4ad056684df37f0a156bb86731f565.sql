-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_name",
    "area",
    "closing_on",
    "detailed_requirements"
FROM "sg-data-d-ba4ad056684df37f0a156bb86731f565"
