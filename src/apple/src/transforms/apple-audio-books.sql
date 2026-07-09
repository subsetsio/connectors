-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are chart snapshots, not a catalog of all audiobooks; the same audiobook can appear in multiple storefronts and snapshots.
SELECT
    "snapshot_date",
    "feed_updated",
    "storefront",
    "media",
    "feed_type",
    "rank",
    CAST("entity_id" AS BIGINT) AS entity_id,
    "name",
    "artist_name",
    CAST("artist_id" AS BIGINT) AS artist_id,
    "artist_url",
    "kind",
    "release_date",
    "content_advisory_rating",
    "genre_names",
    "artwork_url",
    "url"
FROM "apple-audio-books"
