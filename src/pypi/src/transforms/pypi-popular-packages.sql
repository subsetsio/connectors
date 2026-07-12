-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a current popularity snapshot ranked by recent 30-day downloads, not a historical download time series.
SELECT
    "package",
    "rank",
    "download_count_30d",
    CAST("snapshot_last_update" AS TIMESTAMP) AS snapshot_last_update,
    "version",
    "summary",
    "author",
    "author_email",
    "license",
    "license_expression",
    "requires_python",
    "home_page",
    "project_urls",
    "keywords",
    "classifiers",
    "yanked"
FROM "pypi-popular-packages"
