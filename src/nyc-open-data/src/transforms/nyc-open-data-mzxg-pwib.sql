-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "segmentid",
    "bikeid",
    "prevbikeid",
    "status",
    "boro",
    "street",
    "fromstreet",
    "tostreet",
    "onoffst",
    "facilitycl",
    "allclasses",
    "bikedir",
    "lanecount",
    "ft_facilit",
    "tf_facilit",
    "ft2facilit",
    "tf2facilit",
    "instdate",
    "ret_date",
    "grnwy",
    "gwsystem",
    "gwsys2",
    "spur",
    "gwyjuris"
FROM "nyc-open-data-mzxg-pwib"
