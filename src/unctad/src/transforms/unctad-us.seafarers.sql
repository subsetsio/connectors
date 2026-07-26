-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The verifier did not find a compact unique grain; treat rows as report-specific statistical observations and filter all relevant dimensions before aggregating.
SELECT
    CAST("year" AS BIGINT) AS year,
    "economy",
    "economy_label",
    CAST("seafarertype" AS BIGINT) AS seafarertype,
    "seafarertype_label",
    "absolute_value",
    "absolute_value_footnote",
    "absolute_value_missing_value",
    "percentage_of_total_world",
    "percentage_of_total_world_footnote",
    "percentage_of_total_world_missing_value"
FROM "unctad-us.seafarers"
