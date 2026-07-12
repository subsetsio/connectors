-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Birthweight" AS birthweight,
    "Ethnic group" AS ethnic_group,
    "Gestational age completed weeks" AS gestational_age_completed_weeks,
    "Sex" AS sex,
    "WIMD Quintile" AS wimd_quintile,
    "Notes" AS notes
FROM "statswales-dffa216c-41bf-41c6-a93b-93ec494312d8"
