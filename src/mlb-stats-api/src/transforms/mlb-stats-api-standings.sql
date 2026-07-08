SELECT
  CAST(season AS INTEGER) AS season,
  CAST(team_id AS BIGINT) AS team_id,
  CAST(team_name AS VARCHAR) AS team_name,
  CAST(league_id AS BIGINT) AS league_id,
  CAST(division_id AS BIGINT) AS division_id,
  TRY_CAST(division_rank AS INTEGER) AS division_rank,
  TRY_CAST(league_rank AS INTEGER) AS league_rank,
  TRY_CAST(sport_rank AS INTEGER) AS sport_rank,
  TRY_CAST(games_played AS INTEGER) AS games_played,
  TRY_CAST(wins AS INTEGER) AS wins,
  TRY_CAST(losses AS INTEGER) AS losses,
  TRY_CAST(winning_percentage AS DOUBLE) AS winning_percentage,
  CAST(games_back AS VARCHAR) AS games_back,
  TRY_CAST(runs_scored AS INTEGER) AS runs_scored,
  TRY_CAST(runs_allowed AS INTEGER) AS runs_allowed,
  TRY_CAST(run_differential AS INTEGER) AS run_differential,
  CAST(streak AS VARCHAR) AS streak
FROM "mlb-stats-api-standings"
WHERE season IS NOT NULL AND team_id IS NOT NULL
