-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "category",
    "id",
    "metric",
    "_2030_target" AS 2030_target,
    "base_data_year",
    "most_recent_data_year",
    "value_in_base_year",
    "value_in_most_recent_year",
    "change_from_base_year_if_applicable",
    "arrow_direction",
    "status_for_2012_planyc_update",
    "_2000" AS 2000,
    "_2001" AS 2001,
    "_2002" AS 2002,
    "_2003" AS 2003,
    "_2004" AS 2004,
    "_2005" AS 2005,
    "_2006" AS 2006,
    "_2007" AS 2007,
    "_2008" AS 2008,
    "_2009" AS 2009,
    "_2010" AS 2010,
    "_2011" AS 2011,
    "_2012" AS 2012,
    "_2013" AS 2013,
    "agency",
    "additional_source_1",
    "additional_source_2",
    "additional_source_3"
FROM "nyc-open-data-6r4h-c2y6"
