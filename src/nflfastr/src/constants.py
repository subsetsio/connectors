"""Catalog data for the nflfastR connector — which datasets to pull and from
which nflverse-data GitHub release. This is data, not logic; node modules
import it.

ENTITY_IDS is the rank-accepted entity union. ENTITY_TAGS maps each entity to
the GitHub release tag that hosts its parquet assets. Within a release, the
asset filenames whose season-stripped stem equals the entity id are the files
for that entity (one per season, or a single whole-corpus file).
"""

REPO = "nflverse/nflverse-data"

ENTITY_TAGS = {
    "advstats_season_def": "pfr_advstats",
    "advstats_season_pass": "pfr_advstats",
    "advstats_season_rec": "pfr_advstats",
    "advstats_season_rush": "pfr_advstats",
    "advstats_week_def": "pfr_advstats",
    "advstats_week_pass": "pfr_advstats",
    "advstats_week_rec": "pfr_advstats",
    "advstats_week_rush": "pfr_advstats",
    "combine": "combine",
    "depth_charts": "depth_charts",
    "draft_picks": "draft_picks",
    "ftn_charting": "ftn_charting",
    "games": "schedules",
    "historical_contracts": "contracts",
    "injuries": "injuries",
    "ngs_passing": "nextgen_stats",
    "ngs_receiving": "nextgen_stats",
    "ngs_rushing": "nextgen_stats",
    "officials": "officials",
    "pbp_participation": "pbp_participation",
    "play_by_play": "pbp",
    "players": "players",
    "qbr_season_level": "espn_data",
    "qbr_week_level": "espn_data",
    "roster": "rosters",
    "roster_weekly": "weekly_rosters",
    "snap_counts": "snap_counts",
    "stats_player_post": "stats_player",
    "stats_player_reg": "stats_player",
    "stats_player_regpost": "stats_player",
    "stats_player_week": "stats_player",
    "stats_team_post": "stats_team",
    "stats_team_reg": "stats_team",
    "stats_team_regpost": "stats_team",
    "stats_team_week": "stats_team",
    "trades": "trades",
}

ENTITY_IDS = list(ENTITY_TAGS)
