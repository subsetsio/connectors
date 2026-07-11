-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Field of doctorate" AS field_of_doctorate,
    "Total with definite plana" AS total_with_definite_plana,
    "Academe" AS academe,
    "Industry or businessb" AS industry_or_businessb,
    "Government" AS government,
    "Nonprofit organization" AS nonprofit_organization,
    "Other or unknownc" AS other_or_unknownc
FROM "ncses-nsf25349-tab006-007"
