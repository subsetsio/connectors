-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "Measure ID" AS measure_id,
    "Measure Name" AS measure_name,
    CAST("Score" AS DOUBLE) AS score,
    "Footnote - Score" AS footnote_score,
    "National Median" AS national_median,
    "Footnote - National Median" AS footnote_national_median,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date
FROM "cms-3n5g-6b7f"
