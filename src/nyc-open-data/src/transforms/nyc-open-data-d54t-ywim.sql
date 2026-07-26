-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "seatingcho",
    "retailname",
    "bizname",
    "bizdba",
    "biz_desc",
    "other_bizd",
    "bizstreetn",
    "suitenum",
    "bizboro",
    "bizzip",
    "bizaddress",
    "sidewalkdi",
    "sidewalk_1",
    "sidewalkar",
    "openstreet",
    "openstre_1",
    "openstre_2",
    "qualify_si",
    "qualify_op",
    "landmarkdi",
    "landmark_1",
    "healthcomp",
    "submission",
    "creationda",
    "long",
    "lat",
    "x",
    "y"
FROM "nyc-open-data-d54t-ywim"
