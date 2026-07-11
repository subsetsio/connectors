-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Subfield, field, and domain columns are denormalized on each topic row; do not sum topic and parent hierarchy rows together as separate hierarchy levels.
SELECT
    "id",
    "display_name",
    "description",
    CAST("domain_id" AS BIGINT) AS domain_id,
    "domain_name",
    CAST("field_id" AS BIGINT) AS field_id,
    "field_name",
    CAST("subfield_id" AS BIGINT) AS subfield_id,
    "subfield_name",
    "keywords",
    "works_count",
    "cited_by_count",
    "updated_date"
FROM "openalex-topics"
