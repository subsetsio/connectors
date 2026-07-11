-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Agency" AS agency,
    "Total" AS total,
    "Computer sciences and mathematics" AS computer_sciences_and_mathematics,
    "Engineering" AS engineering,
    "Environmental sciences" AS environmental_sciences,
    "Life sciences" AS life_sciences,
    "Physical sciences" AS physical_sciences,
    "Psychology" AS psychology,
    "Social sciences" AS social_sciences,
    "Other sciences nec" AS other_sciences_nec
FROM "ncses-nsf21329-tab077"
