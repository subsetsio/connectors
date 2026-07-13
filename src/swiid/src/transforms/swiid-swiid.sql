-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    "year",
    "gini_disp",
    "gini_disp_se",
    "gini_mkt",
    "gini_mkt_se",
    "abs_red",
    "abs_red_se",
    "rel_red",
    "rel_red_se",
    "release_label",
    "release_description",
    CAST("release_time" AS TIMESTAMP) AS release_time,
    "file_md5"
FROM "swiid-swiid"
