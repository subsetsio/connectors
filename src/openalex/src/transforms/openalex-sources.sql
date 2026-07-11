-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "display_name",
    "issn_l",
    "issn",
    "type",
    "host_organization_name",
    "host_organization",
    "is_oa",
    "is_in_doaj",
    "is_core",
    "country_code",
    "apc_usd",
    "first_publication_year",
    "last_publication_year",
    "works_count",
    "cited_by_count",
    "h_index",
    "i10_index",
    "mean_citedness",
    "created_date",
    "updated_date"
FROM "openalex-sources"
