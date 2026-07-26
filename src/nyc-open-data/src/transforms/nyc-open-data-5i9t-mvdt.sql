-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "new_york_city_debt_outstanding_dollars_in_millions",
    "fy_2020",
    "fy_2019",
    "fy_2018",
    "fy_2017",
    "fy_2016",
    "fy_2015",
    "fy_2014",
    "fy_2013",
    "fy_2012",
    "fy_2011",
    "fy_2010",
    "fy_2009",
    "fy_2008",
    "fy_2007",
    "fy_2006",
    "fy_2005",
    "fy_2004",
    "fy_2003",
    "fy_2002",
    "fy_2001",
    "fy_2000"
FROM "nyc-open-data-5i9t-mvdt"
