-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "commntydst",
    "comp2010ap",
    "comp2010",
    "comp2011",
    "comp2012",
    "comp2013",
    "comp2014",
    "comp2015",
    "comp2016",
    "comp2017",
    "comp2018",
    "comp2019",
    "comp2020",
    "comp2021",
    "comp2022",
    "comp2023",
    "comp2024",
    "cenunits20",
    "filed",
    "approved",
    "permitted",
    "withdrawn",
    "inactive",
    "shape_area",
    "shape_length"
FROM "nyc-open-data-dbdt-5s7j"
