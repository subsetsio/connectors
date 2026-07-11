-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Field of doctorate" AS field_of_doctorate,
    "Total with definite plana - Total" AS total_with_definite_plana_total,
    "Total with definite plana - Male" AS total_with_definite_plana_male,
    "Total with definite plana - Female" AS total_with_definite_plana_female,
    "Employment - Total" AS employment_total,
    "Employment - Male" AS employment_male,
    "Employment - Female" AS employment_female,
    "Postdoctoral study - Total" AS postdoctoral_study_total,
    "Postdoctoral study - Male" AS postdoctoral_study_male,
    "Postdoctoral study - Female" AS postdoctoral_study_female
FROM "ncses-nsf25349-tab006-006"
