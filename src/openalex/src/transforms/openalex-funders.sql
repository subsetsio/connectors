-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "display_name",
    "alternate_titles",
    "country_code",
    "description",
    "homepage_url",
    "works_count",
    "cited_by_count",
    "awards_count",
    "h_index",
    "i10_index",
    "mean_citedness",
    "ror",
    "doi",
    "wikidata",
    "created_date",
    "updated_date"
FROM "openalex-funders"
