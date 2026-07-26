-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "summary_id",
    "num_siam_sprinkler",
    "sprinkler_type",
    "num_siam_standpipe",
    "standpipe_type",
    "num_of_violation_notices",
    "num_of_violation_order",
    "bin",
    "bbl",
    "latitude",
    "longitude",
    "block",
    "lot",
    "borough",
    "community_board",
    "council_district"
FROM "nyc-open-data-nvgj-hbht"
