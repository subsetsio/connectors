-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "PerCent" AS percent,
    "2001",
    "2002",
    "2003",
    "2004",
    "2005",
    "2006",
    "2007",
    "2008",
    "2009",
    "2010",
    "2011",
    "2012",
    "2013",
    "2014",
    "2015",
    "2016",
    "2017",
    "2018",
    "2019",
    "2020",
    "2021",
    "2022",
    "2023",
    "CumulativeChangefrom2013to2023" AS cumulativechangefrom2013to2023,
    "CumulativeChangefrom2013to2018" AS cumulativechangefrom2013to2018,
    "CumulativeChangefrom2018to2023" AS cumulativechangefrom2018to2023,
    "AnnualisedChangefrom2013to2023" AS annualisedchangefrom2013to2023,
    "AnnualisedChangefrom2013to2018" AS annualisedchangefrom2013to2018,
    "AnnualisedChangefrom2018to2023" AS annualisedchangefrom2018to2023
FROM "sg-data-d-5d7f67bcbf2461212a970194d7d13013"
