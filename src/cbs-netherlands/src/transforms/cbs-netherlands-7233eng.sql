-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Sex" AS sex,
    "Age" AS age,
    "CausesOfDeath" AS causesofdeath,
    "Periods" AS periods,
    "Deaths_1" AS deaths_1,
    "Sex_label" AS sex_label,
    "Age_label" AS age_label,
    "CausesOfDeath_label" AS causesofdeath_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-7233eng"
