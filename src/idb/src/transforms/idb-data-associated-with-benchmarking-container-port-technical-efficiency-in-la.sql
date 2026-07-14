-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Puerto" AS puerto,
    "Pais" AS pais,
    CAST("1999" AS DOUBLE) AS "1999",
    CAST("2000" AS DOUBLE) AS "2000",
    CAST("2001" AS DOUBLE) AS "2001",
    CAST("2002" AS DOUBLE) AS "2002",
    CAST("2003" AS DOUBLE) AS "2003",
    CAST("2004" AS DOUBLE) AS "2004",
    CAST("2005" AS DOUBLE) AS "2005",
    CAST("2006" AS DOUBLE) AS "2006",
    CAST("2007" AS DOUBLE) AS "2007",
    CAST("2008" AS DOUBLE) AS "2008",
    CAST("2009" AS DOUBLE) AS "2009",
    CAST("Average" AS DOUBLE) AS average,
    "source_resource"
FROM "idb-data-associated-with-benchmarking-container-port-technical-efficiency-in-la"
