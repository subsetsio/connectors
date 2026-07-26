-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "mangagen",
    "the_geom",
    "projname",
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
FROM "nyc-open-data-dhcf-pcvf"
