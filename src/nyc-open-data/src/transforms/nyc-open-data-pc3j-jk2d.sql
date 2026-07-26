-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "projname",
    "mangagen",
    "orrid",
    "onenyc",
    "projval",
    "schedule",
    "compdate",
    "fndsourc",
    "borough",
    "coundist",
    "commbord",
    "moreinfo",
    "link"
FROM "nyc-open-data-pc3j-jk2d"
