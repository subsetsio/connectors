-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sample_date",
    "test_date",
    "wrrf_name",
    "wrrf_abbreviation",
    "concentration_sarscov2_gene_target_n1_copiesl",
    "per_capita_sarscov2_load_n1_copies_per_day_per_population",
    "annotation",
    "population_served_estimated",
    "technology"
FROM "nyc-open-data-f7dc-2q9f"
