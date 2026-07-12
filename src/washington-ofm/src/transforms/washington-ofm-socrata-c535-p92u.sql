-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_entity_id" AS entity_id,
    "_source_type" AS source_type,
    "_socrata_dataset_id" AS socrata_dataset_id,
    "county_name",
    CAST("popden_2000" AS DOUBLE) AS popden_2000,
    CAST("popden_2001" AS DOUBLE) AS popden_2001,
    CAST("popden_2002" AS DOUBLE) AS popden_2002,
    CAST("popden_2003" AS DOUBLE) AS popden_2003,
    CAST("popden_2004" AS DOUBLE) AS popden_2004,
    CAST("popden_2005" AS DOUBLE) AS popden_2005,
    CAST("popden_2006" AS DOUBLE) AS popden_2006,
    CAST("popden_2007" AS DOUBLE) AS popden_2007,
    CAST("popden_2008" AS DOUBLE) AS popden_2008,
    CAST("popden_2009" AS DOUBLE) AS popden_2009,
    CAST("popden_2010" AS DOUBLE) AS popden_2010,
    CAST("popden_2011" AS DOUBLE) AS popden_2011,
    CAST("popden_2012" AS DOUBLE) AS popden_2012,
    CAST("popden_2013" AS DOUBLE) AS popden_2013,
    CAST("popden_2014" AS DOUBLE) AS popden_2014,
    CAST("popden_2015" AS DOUBLE) AS popden_2015,
    CAST("popden_2016" AS DOUBLE) AS popden_2016,
    CAST("popden_2017" AS DOUBLE) AS popden_2017,
    CAST("popden_2018" AS DOUBLE) AS popden_2018,
    CAST("popden_2019" AS DOUBLE) AS popden_2019,
    CAST("popden_2020" AS DOUBLE) AS popden_2020,
    CAST("popden_2021" AS DOUBLE) AS popden_2021,
    CAST("popden_2022" AS DOUBLE) AS popden_2022,
    CAST("popden_2023" AS DOUBLE) AS popden_2023,
    CAST("popden_2024" AS DOUBLE) AS popden_2024,
    CAST("popden_2025" AS DOUBLE) AS popden_2025
FROM "washington-ofm-socrata-c535-p92u"
