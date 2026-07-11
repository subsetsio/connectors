-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Agency" AS agency,
    "Total" AS total,
    "Atmospheric sciences" AS atmospheric_sciences,
    "Geological sciences" AS geological_sciences,
    "Oceanography" AS oceanography,
    "Other environmental sciences" AS other_environmental_sciences
FROM "ncses-nsf21329-tab022"
