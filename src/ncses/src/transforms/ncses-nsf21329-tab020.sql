-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Agency" AS agency,
    "Total" AS total,
    "Computer sciences" AS computer_sciences,
    "Mathematics" AS mathematics,
    "Other computer sciences and mathematics" AS other_computer_sciences_and_mathematics
FROM "ncses-nsf21329-tab020"
