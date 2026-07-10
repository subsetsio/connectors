-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "Measure ID" AS measure_id,
    "Measure Name" AS measure_name,
    "National Rate" AS national_rate,
    CAST("Number of Hospitals Worse" AS BIGINT) AS number_of_hospitals_worse,
    CAST("Number of Hospitals Same" AS BIGINT) AS number_of_hospitals_same,
    CAST("Number of Hospitals Better" AS BIGINT) AS number_of_hospitals_better,
    CAST("Number of Hospitals Too Few" AS BIGINT) AS number_of_hospitals_too_few,
    CAST("Footnote" AS BIGINT) AS footnote,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date
FROM "cms-uk3n-au7a"
