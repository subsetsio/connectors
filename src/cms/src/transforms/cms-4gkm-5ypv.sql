-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "State" AS state,
    "Measure ID" AS measure_id,
    "Measure Name" AS measure_name,
    "Number of Hospitals Worse" AS number_of_hospitals_worse,
    "Number of Hospitals Same" AS number_of_hospitals_same,
    "Number of Hospitals Better" AS number_of_hospitals_better,
    "Number of Hospitals Too Few" AS number_of_hospitals_too_few,
    "Footnote" AS footnote,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    "Number of Hospitals Fewer" AS number_of_hospitals_fewer,
    "Number of Hospitals Average" AS number_of_hospitals_average,
    "Number of Hospitals More" AS number_of_hospitals_more,
    "Number of Hospitals Too Small" AS number_of_hospitals_too_small
FROM "cms-4gkm-5ypv"
