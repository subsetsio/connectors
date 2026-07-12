-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "Level" AS level,
    "Description" AS description,
    "SeriesRefSNDQ" AS seriesrefsndq,
    "Quarter" AS quarter,
    CAST("Weight" AS DOUBLE) AS weight,
    CAST("Amount" AS DOUBLE) AS amount
FROM "statsnz-gross-domestic-product-march-2026-quarter-visualisation"
