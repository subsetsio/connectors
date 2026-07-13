-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Programs" AS programs,
    CAST("1993" AS DOUBLE) AS 1993,
    CAST("1994" AS DOUBLE) AS 1994,
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
    CAST("2012" AS DOUBLE) AS 2012,
    CAST("2013" AS DOUBLE) AS 2013,
    CAST("2014" AS DOUBLE) AS 2014,
    CAST("2015" AS DOUBLE) AS 2015,
    "source_resource"
FROM "idb-non-contributory-public-spending-in-latin-america-and-the-caribbean-data-20"
