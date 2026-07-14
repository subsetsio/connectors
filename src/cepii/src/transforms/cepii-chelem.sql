-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: CHELEM is stored wide by year, so year-specific measures are separate columns rather than one row per year.
SELECT
    "exporter",
    "importer",
    "secgroup",
    "product",
    "v2000",
    "v2001",
    "v2002",
    "v2003",
    "v2004",
    "v2005",
    "v2006",
    "v2007",
    "v2008",
    "v2009",
    "v2010",
    "v2011",
    "v2012",
    "v2013",
    "v2014",
    "v2015",
    "v2016",
    "v2017",
    "v2018",
    "v2019",
    "v2020",
    "v2021",
    "v2022",
    "v2023"
FROM "cepii-chelem"
