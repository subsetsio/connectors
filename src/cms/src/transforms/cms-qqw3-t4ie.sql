-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Measure ID" AS measure_id,
    "Measure Name" AS measure_name,
    CAST("National Rate" AS DOUBLE) AS national_rate,
    CAST("Number of Hospitals Worse" AS BIGINT) AS number_of_hospitals_worse,
    CAST("Number of Hospitals Same" AS BIGINT) AS number_of_hospitals_same,
    CAST("Number of Hospitals Better" AS BIGINT) AS number_of_hospitals_better,
    "Number of Hospitals Too Few" AS number_of_hospitals_too_few,
    "Footnote" AS footnote,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date
FROM "cms-qqw3-t4ie"
