-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Metrics are summed across all packages attributed to each maintainer, so they should not be compared directly to per-package rows without accounting for this aggregation level.
SELECT
    "rank",
    "name",
    "inst",
    "vote",
    "old",
    "recent",
    "no_files",
    "maintainer"
FROM "debian-popcon-maintainers"
