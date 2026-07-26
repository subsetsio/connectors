-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The verifier did not find a compact unique grain; treat rows as report-specific statistical observations and filter all relevant dimensions before aggregating.
SELECT
    CAST("year" AS BIGINT) AS year,
    "economy",
    "economy_label",
    "processfoodcategory",
    "processfoodcategory_label",
    "rca_food_process",
    "rca_food_process_footnote",
    "rca_food_process_missing_value"
FROM "unctad-us.tradefoodproccat-cat-rca"
