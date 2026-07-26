-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "hudson_river_greenway_b",
    "riverside_drive_a",
    "west_end_ave_a",
    "broadway_a",
    "amsterdam_ave_b",
    "columbus_ave_b",
    "central_park_west_a",
    "central_park_dr_west",
    "central_park_dr_east",
    "_5th_ave" AS 5th_ave,
    "madison_ave",
    "park_ave_a",
    "lexington_ave",
    "_3rd_ave" AS 3rd_ave,
    "_2nd_ave_b" AS 2nd_ave_b,
    "_1st_ave_b" AS 1st_ave_b,
    "york_ave_a",
    "east_end_ave_a",
    "east_river_greenway_b",
    "total"
FROM "nyc-open-data-tgzg-ssan"
