-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Agency" AS agency,
    "Total" AS total,
    "Agricultural sciences" AS agricultural_sciences,
    "Biological sciences excluding environmental biology" AS biological_sciences_excluding_environmental_biology,
    "Environmental biology" AS environmental_biology,
    "Medical sciences" AS medical_sciences,
    "Other life sciences" AS other_life_sciences
FROM "ncses-nsf21329-tab082"
