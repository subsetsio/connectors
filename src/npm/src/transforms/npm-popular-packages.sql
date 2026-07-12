-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is a popularity-ranked search snapshot, not a complete registry inventory.
SELECT
    "name",
    "version",
    "description",
    "license",
    CAST("date" AS TIMESTAMP) AS date,
    "publisher_username",
    "maintainers_count",
    "keywords",
    "repository_url",
    "homepage_url",
    "npm_url",
    "monthly_downloads",
    "weekly_downloads",
    "dependents_count",
    "search_score"
FROM "npm-popular-packages"
