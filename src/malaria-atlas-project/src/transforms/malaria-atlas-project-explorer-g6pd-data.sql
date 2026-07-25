-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are survey observations for G6PD deficiency data and should not be interpreted as administrative-area totals.
SELECT
    "id",
    "country",
    "latitude",
    "longitude",
    "area_type",
    "sexes",
    "number_males",
    "number_males_deficient",
    "number_females",
    "number_females_deficient",
    "citation",
    "area_size",
    "country_id",
    "malaria_metrics_available",
    "_source_type_name" AS source_type_name,
    "_feature_id" AS feature_id,
    "_geometry_name" AS geometry_name,
    "_geometry" AS geometry,
    "_bbox" AS bbox
FROM "malaria-atlas-project-explorer:g6pd-data"
