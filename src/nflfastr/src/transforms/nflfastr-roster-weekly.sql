-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Weekly roster rows are player-team-week snapshots; aggregate after selecting a season/week context.
SELECT
    "season",
    "team",
    "position",
    "depth_chart_position",
    "jersey_number",
    "status",
    "full_name",
    "first_name",
    "last_name",
    "birth_date",
    "height",
    "weight",
    "college",
    "gsis_id",
    CAST("espn_id" AS BIGINT) AS espn_id,
    "sportradar_id",
    "yahoo_id",
    CAST("rotowire_id" AS BIGINT) AS rotowire_id,
    CAST("pff_id" AS BIGINT) AS pff_id,
    "pfr_id",
    CAST("fantasy_data_id" AS BIGINT) AS fantasy_data_id,
    CAST("sleeper_id" AS BIGINT) AS sleeper_id,
    "years_exp",
    "headshot_url",
    "ngs_position",
    "week",
    "game_type",
    "status_description_abbr",
    "football_name",
    "esb_id",
    CAST("gsis_it_id" AS BIGINT) AS gsis_it_id,
    "smart_id",
    "entry_year",
    "rookie_year",
    "draft_club",
    CAST("draft_number" AS BIGINT) AS draft_number
FROM "nflfastr-roster-weekly"
