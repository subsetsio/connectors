-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Enrollment" AS enrollment,
    CAST("2001" AS BIGINT) AS "2001",
    CAST("2002" AS BIGINT) AS "2002",
    CAST("2003" AS BIGINT) AS "2003",
    CAST("2004" AS BIGINT) AS "2004",
    "2005",
    "2006",
    "2007",
    "2008",
    "2009",
    "2010",
    "2011",
    CAST("2012" AS BIGINT) AS "2012",
    "2013",
    "2014",
    "2015",
    "2016",
    "2017",
    "2018",
    "2019",
    CAST("2020" AS BIGINT) AS "2020",
    CAST("2021" AS BIGINT) AS "2021",
    CAST("2022" AS BIGINT) AS "2022"
FROM "instituto-de-estad-sticas-de-puerto-rico-matricula-historica-rev-2016-conservatorio-de-musica"
