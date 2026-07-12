-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are directional monthly country-to-country flows; reversing country_from and country_to changes the measure.
SELECT
    "country_from",
    "country_to",
    strptime("migration_month", '%Y-%m')::DATE AS migration_month,
    "num_migrants",
    "_source_file" AS source_file
FROM "meta-international-migration-flows"
