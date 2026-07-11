-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Field and domain columns are denormalized on each subfield row; do not sum subfield, field, and domain rows together as separate hierarchy levels.
SELECT
    CAST("id" AS BIGINT) AS id,
    "display_name",
    "description",
    CAST("domain_id" AS BIGINT) AS domain_id,
    "domain_name",
    CAST("field_id" AS BIGINT) AS field_id,
    "field_name",
    "wikidata",
    "topics",
    "works_count",
    "cited_by_count",
    "updated_date"
FROM "openalex-subfields"
