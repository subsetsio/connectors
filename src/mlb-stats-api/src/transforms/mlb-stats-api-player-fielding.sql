SELECT
  CAST(season AS INTEGER) AS season,
  CAST(player_id AS BIGINT) AS player_id,
  CAST(player_name AS VARCHAR) AS player_name,
  CAST(team_id AS BIGINT) AS team_id,
  CAST(team_name AS VARCHAR) AS team_name,
  CAST(league_id AS BIGINT) AS league_id,
  CAST(position_code AS VARCHAR) AS position_code,
  CAST(position_name AS VARCHAR) AS position_name,
  CAST(position_abbreviation AS VARCHAR) AS position_abbreviation,
  TRY_CAST("gamesPlayed" AS BIGINT) AS "gamesPlayed",
  TRY_CAST("gamesStarted" AS BIGINT) AS "gamesStarted",
  TRY_CAST("assists" AS BIGINT) AS "assists",
  TRY_CAST("putOuts" AS BIGINT) AS "putOuts",
  TRY_CAST("errors" AS BIGINT) AS "errors",
  TRY_CAST("chances" AS BIGINT) AS "chances",
  TRY_CAST("doublePlays" AS BIGINT) AS "doublePlays",
  TRY_CAST("triplePlays" AS BIGINT) AS "triplePlays",
  TRY_CAST("fielding" AS DOUBLE) AS "fielding",
  TRY_CAST("rangeFactorPerGame" AS DOUBLE) AS "rangeFactorPerGame",
  TRY_CAST("rangeFactorPer9Inn" AS DOUBLE) AS "rangeFactorPer9Inn",
  CAST("innings" AS VARCHAR) AS "innings"
FROM "mlb-stats-api-player-fielding"
WHERE season IS NOT NULL
