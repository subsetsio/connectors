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
    "2024",
    "CumulativeChangefrom2014to2024" AS cumulativechangefrom2014to2024,
    "CumulativeChangefrom2014to2019" AS cumulativechangefrom2014to2019,
    "CumulativeChangefrom2019to2024" AS cumulativechangefrom2019to2024,
    "AnnualisedChangefrom2014to2024" AS annualisedchangefrom2014to2024,
    "AnnualisedChangefrom2014to2019" AS annualisedchangefrom2014to2019,
    "AnnualisedChangefrom2019to2024" AS annualisedchangefrom2019to2024
FROM "sg-data-d-58af85d446af2cc669920a2dffcfbe4e"
