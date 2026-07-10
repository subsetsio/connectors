-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Player" AS player,
    "Position" AS position,
    "ID" AS id,
    "Draft Year" AS draft_year,
    "Projected SPM" AS projected_spm,
    "Superstar" AS superstar,
    "Starter" AS starter,
    "Role Player" AS role_player,
    "Bust" AS bust
FROM "fivethirtyeight-nba-draft-2015-historical-projections"
