-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows describe directed region-to-region social connectedness pairs; user and friend regions are not interchangeable.
SELECT
    "user_country",
    "friend_country",
    "user_region",
    "friend_region",
    "scaled_sci",
    "_source_file" AS source_file
FROM "meta-social-connectedness-index"
