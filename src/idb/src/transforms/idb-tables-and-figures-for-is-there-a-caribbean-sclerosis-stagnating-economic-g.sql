-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Country_Name" AS country_name,
    "1991",
    "1992",
    "1993",
    "1994",
    CAST("1995" AS DOUBLE) AS 1995,
    CAST("1996" AS DOUBLE) AS 1996,
    CAST("1997" AS DOUBLE) AS 1997,
    CAST("1998" AS DOUBLE) AS 1998,
    CAST("1999" AS DOUBLE) AS 1999,
    CAST("2000" AS DOUBLE) AS 2000,
    CAST("2001" AS DOUBLE) AS 2001,
    CAST("2002" AS DOUBLE) AS 2002,
    CAST("2003" AS DOUBLE) AS 2003,
    CAST("2004" AS DOUBLE) AS 2004,
    CAST("2005" AS DOUBLE) AS 2005,
    CAST("2006" AS DOUBLE) AS 2006,
    CAST("2007" AS DOUBLE) AS 2007,
    CAST("2008" AS DOUBLE) AS 2008,
    CAST("2009" AS DOUBLE) AS 2009,
    CAST("2010" AS DOUBLE) AS 2010,
    CAST("2011" AS DOUBLE) AS 2011,
    "2012",
    "None" AS none,
    "source_resource"
FROM "idb-tables-and-figures-for-is-there-a-caribbean-sclerosis-stagnating-economic-g"
