-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Agency" AS agency,
    "Total" AS total,
    "Anthropology" AS anthropology,
    "Economics" AS economics,
    "Political science" AS political_science,
    "Sociology" AS sociology,
    "Other social sciences" AS other_social_sciences
FROM "ncses-nsf21329-tab026"
