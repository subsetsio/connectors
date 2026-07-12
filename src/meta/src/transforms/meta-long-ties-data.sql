-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table combines different geographic unit files; include _source_file and unit when comparing or joining unit_id values.
SELECT
    "unit_id",
    "mean_degree",
    "clustering_coef",
    "weighted_clustering_coef",
    "fraction_long_edges",
    "weighted_fraction_long_edges",
    "country",
    "unit",
    "_source_file" AS source_file
FROM "meta-long-ties-data"
