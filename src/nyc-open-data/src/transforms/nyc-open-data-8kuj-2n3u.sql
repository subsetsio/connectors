-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "borocode",
    "boroname",
    "borocd",
    "coundist",
    "assemdist",
    "stsendist",
    "congdist",
    "main_street",
    "cross_street",
    "barnes_dance",
    "modified_barnes_dance",
    "midblock_crossing",
    "t_oneway_away_24_hour_walk",
    "t_oneway_away_all_walk_in_phase_b",
    "installation_date",
    "ntaname",
    "femafldz",
    "femafldt",
    "hrcevac"
FROM "nyc-open-data-8kuj-2n3u"
