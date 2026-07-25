-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are site-level dominant vector occurrence survey observations and may include multiple observations for the same place, species, or time period.
SELECT
    "id",
    "site_id",
    "latitude",
    "longitude",
    "country",
    "country_id",
    "continent_id",
    "month_start",
    "year_start",
    "month_end",
    "year_end",
    "anopheline_id",
    "species",
    "species_plain",
    "id_method1",
    "id_method2",
    "sample_method1",
    "sample_method2",
    "sample_method3",
    "sample_method4",
    "assi",
    "citation",
    "time_start",
    "time_end",
    "_source_type_name" AS source_type_name,
    "_feature_id" AS feature_id,
    "_geometry_name" AS geometry_name,
    "_geometry" AS geometry,
    "_bbox" AS bbox
FROM "malaria-atlas-project-vector-occurrence:201201-global-dominant-vector-surveys"
