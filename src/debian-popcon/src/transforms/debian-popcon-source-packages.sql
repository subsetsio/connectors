-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Metrics are summed across binary packages built by each source package; use the source-packages-max table when a maximum-over-binaries measure is needed instead.
SELECT
    "rank",
    "name",
    "inst",
    "vote",
    "old",
    "recent",
    "no_files",
    "maintainer"
FROM "debian-popcon-source-packages"
