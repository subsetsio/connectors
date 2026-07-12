-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a current catalog snapshot: downloads, likes, trending score, tags, and repository metadata describe the repository at crawl time and do not provide historical changes.
SELECT
    "id",
    "author",
    "downloads",
    "likes",
    "trendingScore" AS trendingscore,
    "pipeline_tag",
    "library_name",
    "gated",
    "private",
    CAST("createdAt" AS TIMESTAMP) AS createdat,
    CAST("lastModified" AS TIMESTAMP) AS lastmodified,
    "tags"
FROM "huggingface-models"
