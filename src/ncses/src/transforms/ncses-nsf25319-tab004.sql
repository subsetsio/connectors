-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Field" AS field,
    "NASF millions a" AS nasf_millions_a,
    "Condition % NASF - Superior" AS condition_nasf_superior,
    "Condition % NASF - Satisfactory" AS condition_nasf_satisfactory,
    "Condition % NASF - Requires renovations" AS condition_nasf_requires_renovations,
    "Condition % NASF - Requires replacement" AS condition_nasf_requires_replacement
FROM "ncses-nsf25319-tab004"
