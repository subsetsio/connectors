-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Raw Statistik Nord table preserved as an independent source publication; consumers should inspect column meanings and aggregation levels before combining across tables.
SELECT
    "entity_id",
    "release_title",
    "source_package_id",
    "source_url",
    "measure",
    "date",
    "year",
    "month",
    "value"
FROM "statistik-nord-verbraucherpreisindex-schleswig-holstein-juni-2026"
