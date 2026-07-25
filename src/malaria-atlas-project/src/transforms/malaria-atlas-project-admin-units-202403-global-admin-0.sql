-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Country boundary records are reference geography, not observations; join or filter by admin level before combining with subnational series.
SELECT
    "gid",
    "iso",
    "admn_level",
    "name_0",
    "id_0",
    "code_0",
    "type_0",
    "source",
    "iso2",
    "_source_type_name" AS source_type_name,
    "_feature_id" AS feature_id,
    "_geometry_name" AS geometry_name,
    "_geometry" AS geometry,
    "_bbox" AS bbox
FROM "malaria-atlas-project-admin-units:202403-global-admin-0"
