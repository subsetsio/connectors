-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Pull and star counts are cumulative lifetime totals observed at each snapshot_date; differences between snapshots approximate change over time.
SELECT
    strptime("snapshot_date", '%Y-%m-%d')::DATE AS snapshot_date,
    "namespace",
    "repo",
    "pull_count",
    "star_count",
    CAST("last_updated" AS TIMESTAMP) AS last_updated
FROM "docker-hub-pull-stats"
