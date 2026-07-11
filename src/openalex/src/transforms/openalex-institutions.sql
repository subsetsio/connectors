-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The verified grain includes created_date because the landed snapshot contains institution identifiers in combination with their creation date; join to other OpenAlex data on id with awareness that id alone was not verified as the row key in this raw asset.
SELECT
    "id",
    "display_name",
    "ror",
    "type",
    "country_code",
    "homepage_url",
    "city",
    "region",
    "geo_country",
    "latitude",
    "longitude",
    "works_count",
    "cited_by_count",
    "h_index",
    "i10_index",
    "mean_citedness",
    "created_date",
    "updated_date"
FROM "openalex-institutions"
