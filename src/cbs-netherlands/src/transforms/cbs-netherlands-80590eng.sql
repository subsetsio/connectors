-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Sex" AS sex,
    "Age" AS age,
    "Periods" AS periods,
    "NotSeasonallyAdjusted_1" AS notseasonallyadjusted_1,
    "SeasonallyAdjusted_2" AS seasonallyadjusted_2,
    "NotSeasonallyAdjusted_3" AS notseasonallyadjusted_3,
    "SeasonallyAdjusted_4" AS seasonallyadjusted_4,
    "NotSeasonallyAdjusted_5" AS notseasonallyadjusted_5,
    "SeasonallyAdjusted_6" AS seasonallyadjusted_6,
    "NotSeasonallyAdjusted_7" AS notseasonallyadjusted_7,
    "SeasonallyAdjusted_8" AS seasonallyadjusted_8,
    "NotSeasonallyAdjusted_9" AS notseasonallyadjusted_9,
    "SeasonallyAdjusted_10" AS seasonallyadjusted_10,
    "NotSeasonallyAdjusted_11" AS notseasonallyadjusted_11,
    "SeasonallyAdjusted_12" AS seasonallyadjusted_12,
    "NotSeasonallyAdjusted_13" AS notseasonallyadjusted_13,
    "SeasonallyAdjusted_14" AS seasonallyadjusted_14,
    "Sex_label" AS sex_label,
    "Age_label" AS age_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-80590eng"
