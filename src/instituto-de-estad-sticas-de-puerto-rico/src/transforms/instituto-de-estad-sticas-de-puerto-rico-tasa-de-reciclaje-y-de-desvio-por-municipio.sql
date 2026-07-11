-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Municipio" AS municipio,
    "2006_STD" AS 2006_std,
    "2006_TD" AS 2006_td,
    "2006_STD%" AS 2006_std_2,
    "2006_TD%" AS 2006_td_2,
    "2009_STD" AS 2009_std,
    "2009_TD" AS 2009_td,
    "2009_STD%" AS 2009_std_2,
    "2009_TD%" AS 2009_td_2,
    "2010_STD" AS 2010_std,
    "2010_TD" AS 2010_td,
    "2010_STD%" AS 2010_std_2,
    "2010_TD%" AS 2010_td_2,
    "2011_STD" AS 2011_std,
    "2011_TD" AS 2011_td,
    "2011_STD%" AS 2011_std_2,
    "2011_TD%" AS 2011_td_2,
    "2012_STD" AS 2012_std,
    "2012_TD" AS 2012_td,
    "2012_STD%" AS 2012_std_2,
    "2012_TD%" AS 2012_td_2,
    "2013_STD" AS 2013_std,
    "2013_TD" AS 2013_td,
    "2013_STD%" AS 2013_std_2,
    "2013_TD%" AS 2013_td_2,
    "2014_STD" AS 2014_std,
    "2014_TD" AS 2014_td,
    "2014_STD%" AS 2014_std_2,
    "2014_TD%" AS 2014_td_2
FROM "instituto-de-estad-sticas-de-puerto-rico-tasa-de-reciclaje-y-de-desvio-por-municipio"
