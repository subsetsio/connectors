-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(W1)" AS tlist_w1,
    "Week ending date" AS week_ending_date,
    "SEX" AS sex,
    "Sex Label" AS sex_label,
    "AGE" AS age,
    "Age band" AS age_band,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "nisra-wdthssxag"
