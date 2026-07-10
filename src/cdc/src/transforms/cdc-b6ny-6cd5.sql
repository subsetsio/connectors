-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Current_season" AS current_season,
    "Month" AS month,
    "Previous_flu_Season" AS previous_flu_season,
    "Jurisdiction" AS jurisdiction,
    CAST("2025_26_estimate" AS DOUBLE) AS 2025_26_estimate,
    "Previous_Estimate" AS previous_estimate,
    "Difference_in_season_estimate" AS difference_in_season_estimate,
    "Numerator" AS numerator,
    "Previous_season_numerator" AS previous_season_numerator,
    CAST("Population" AS BIGINT) AS population,
    "Age_group_label" AS age_group_label,
    "Difference_indicator" AS difference_indicator,
    "Child_or_adult" AS child_or_adult
FROM "cdc-b6ny-6cd5"
