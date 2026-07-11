-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Agency" AS agency,
    "Total" AS total,
    "Biological aspects" AS biological_aspects,
    "Social aspects" AS social_aspects,
    "Other psychological sciences" AS other_psychological_sciences
FROM "ncses-nsf21329-tab064"
