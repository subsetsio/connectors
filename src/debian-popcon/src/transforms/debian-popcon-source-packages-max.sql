-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Metrics are the maximum observed among binary packages for each source package rather than a sum; use the source-packages table for summed counts.
SELECT
    "rank",
    "name",
    "inst",
    "vote",
    "old",
    "recent",
    "no_files",
    "maintainer"
FROM "debian-popcon-source-packages-max"
