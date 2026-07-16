-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Sex" AS sex,
    "Age31December" AS age31december,
    "Periods" AS periods,
    "Deaths_1" AS deaths_1,
    "Sex_label" AS sex_label,
    "Age31December_label" AS age31december_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-70895eng"
