-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "FinancialYear" AS financialyear,
    CAST("NumOfWomenWithLiveBirth" AS BIGINT) AS numofwomenwithlivebirth,
    CAST("NumOfResultWomenWithLiveBirth" AS BIGINT) AS numofresultwomenwithlivebirth,
    CAST("NumOfPositiveResultWomenWithLiveBirth" AS BIGINT) AS numofpositiveresultwomenwithlivebirth,
    CAST("NumOfNegativeResultWomenWithLiveBirth" AS BIGINT) AS numofnegativeresultwomenwithlivebirth,
    CAST("PcPositiveResultWomenWithLiveBirth" AS DOUBLE) AS pcpositiveresultwomenwithlivebirth,
    CAST("PcNegativeResultWomenWithLiveBirth" AS DOUBLE) AS pcnegativeresultwomenwithlivebirth,
    CAST("NumOfAllWomen" AS BIGINT) AS numofallwomen,
    CAST("NumOfResultAllWomen" AS BIGINT) AS numofresultallwomen,
    CAST("NumOfPositiveResultAllWomen" AS BIGINT) AS numofpositiveresultallwomen,
    CAST("NumOfNegativeResultAllWomen" AS BIGINT) AS numofnegativeresultallwomen,
    CAST("PcPositiveResultAllWomen" AS DOUBLE) AS pcpositiveresultallwomen,
    CAST("PcNegativeResultAllWomen" AS DOUBLE) AS pcnegativeresultallwomen,
    "HBR" AS hbr,
    CAST("PcResultWomenWithLiveBirth" AS DOUBLE) AS pcresultwomenwithlivebirth,
    CAST("PcResultAllWomen" AS DOUBLE) AS pcresultallwomen
FROM "public-health-scotland-pregnancy-infectious-diseases-screening-in-scotland"
