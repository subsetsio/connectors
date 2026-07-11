-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Field" AS field,
    "2019",
    "2020 preliminary" AS 2020_preliminary
FROM "ncses-nsf21329-tab029"
