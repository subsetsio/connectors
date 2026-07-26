-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "indicator_name",
    "_2003" AS 2003,
    "_2004" AS 2004,
    "_2005" AS 2005,
    "_2006" AS 2006,
    "_2007" AS 2007,
    "_2008" AS 2008,
    "_2009" AS 2009,
    "_2010" AS 2010,
    "_2011" AS 2011,
    "_2012" AS 2012
FROM "nyc-open-data-jhjm-vsp8"
