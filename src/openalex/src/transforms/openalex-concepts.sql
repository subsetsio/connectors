-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: OpenAlex marks concepts as deprecated in favor of the topic classification; use topic tables for current subject taxonomy work.
SELECT
    "id",
    "display_name",
    "description",
    "level",
    "wikidata",
    "ancestors",
    "related_concepts",
    "works_count",
    "cited_by_count",
    "h_index",
    "i10_index",
    "mean_citedness",
    "updated_date"
FROM "openalex-concepts"
