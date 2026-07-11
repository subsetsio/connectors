-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "feature_id",
    "id",
    "title_en",
    "title_fr",
    "abstract_en",
    "abstract_fr",
    "documentation_url_en",
    "documentation_url_fr",
    "geometry_type",
    "geometry_json"
FROM "environment-and-climate-change-canada-datasets-footprints"
