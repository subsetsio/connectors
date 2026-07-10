SELECT
    CAST("aggGenLT2000" AS VARCHAR) AS "aggGenLT2000",
    CAST("aggID" AS VARCHAR) AS "aggID",
    CAST("aucAggCode" AS VARCHAR) AS "aucAggCode",
    CAST("aucAggName" AS VARCHAR) AS "aucAggName",
    CAST("aucMethodPercEnteringUWWTP" AS VARCHAR) AS "aucMethodPercEnteringUWWTP",
    CAST("aucPercC2T" AS VARCHAR) AS "aucPercC2T",
    CAST("aucPercEnteringUWWTP" AS VARCHAR) AS "aucPercEnteringUWWTP",
    CAST("aucUwwCode" AS VARCHAR) AS "aucUwwCode",
    CAST("aucUwwName" AS VARCHAR) AS "aucUwwName",
    CAST("aucUWWTP_AggloID" AS VARCHAR) AS "aucUWWTP_AggloID",
    CAST("CountryCode" AS VARCHAR) AS "CountryCode",
    CAST("repCode" AS VARCHAR) AS "repCode",
    CAST("rptMStateKey" AS VARCHAR) AS "rptMStateKey"
FROM "european-environment-agency-wise-uwwtd.t-uwwtpagglos"
