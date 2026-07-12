-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sports_activity",
    "lnsht_lrydy",
    "adults_lnsht_lrydy",
    "youth_lshbb",
    "junior_under_18_lnshy_yn",
    "junior_under_16_l_shbl",
    "kids_lsgr"
FROM "qatar-planning-and-statistics-authority-arab-championships-by-sports-activity-and-age-groups-2021-2022"
