-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "version https://git-lfs.github.com/spec/v1" AS version_https_git_lfs_github_com_spec_v1
FROM "fivethirtyeight-scrabble-games-scrabble-games"
