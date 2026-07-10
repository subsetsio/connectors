-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("grossregion" AS VARCHAR) AS "grossregion",
    CAST("wirtschaftsabteilung" AS VARCHAR) AS "wirtschaftsabteilung",
    CAST("schweizer_innen_und_ausländer_innen" AS VARCHAR) AS "schweizer_innen_und_ausländer_innen",
    CAST("dienstjahre" AS VARCHAR) AS "dienstjahre",
    CAST("zentralwert_und_andere_perzentile" AS VARCHAR) AS "zentralwert_und_andere_perzentile",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0304010000-206"
